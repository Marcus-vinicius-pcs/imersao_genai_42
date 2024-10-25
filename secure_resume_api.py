import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
import chromadb
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from functools import wraps
from langchain.embeddings import HuggingFaceEmbeddings
import torch

# Crie a aplicação Flask
app = Flask(__name__)
CORS(app)

# Define o diretório de uploads
app.config['UPLOAD_FOLDER'] = 'uploads'

# Crie o diretório de uploads se ele não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configura o Flask Limiter
limiter = Limiter(
    app=app,
    default_limits=["200 per minute", "1000 per day"],
    key_func=get_remote_address
)

# ChromaDB Setup (usando o LLaMA para embeddings)
client = chromadb.Client()
collection = client.create_collection(name="curriculos")
embeddings = HuggingFaceEmbeddings(model_name="facebook/bart-large-cnn", model_kwargs={'device': torch.device('cuda' if torch.cuda.is_available() else 'cpu')})


def embed_function(input):  # Accept 'input' as a keyword argument
    if isinstance(input, list):
        # Process each input separately
        return [embeddings.embed_query(doc) for doc in input]
    else:
        return embeddings.embed_query(input)

collection._embedding_function = embed_function


# Define papéis e permissões
ROLES = {
    "candidato": {"upload_pdf": True, "search": True, "delete_curriculum": False},
    "recrutador": {"upload_pdf": False, "search": True, "delete_curriculum": False},
    "administrador": {"upload_pdf": True, "search": True, "delete_curriculum": True}
}

# Autenticação e Autorização
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Autenticação necessária"}), 401
        token = auth_header.split(" ")[1]
        if token == "candidato_token":
            return func(*args, **kwargs, role="candidato")
        elif token == "recrutador_token":
            return func(*args, **kwargs, role="recrutador")
        elif token == "administrador_token":
            return func(*args, **kwargs, role="administrador")
        else:
            return jsonify({"error": "Token inválido"}), 401
    return wrapper

# Upload de PDF com Limitação de Taxa
@limiter.limit("2 per minute/user")
@app.route('/upload_pdf', methods=['POST'])
@authenticate
def upload_pdf(role):
    if not ROLES[role]["upload_pdf"]:
        return jsonify({"error": "Acesso não autorizado"}), 403
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "Nenhum arquivo encontrado"}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Extração de texto do PDF
    text = extract_text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Chunking usando RecursiveCharacterTextSplitter
    chunks = chunk_text_recursive(text, chunk_size=500, chunk_overlap=50, separators=['. ', '\n\n'])

    # Armazena chunks no ChromaDB
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=chunks,  # This should already be a list
            metadatas=[{"document": filename, "chunk": i} for i in range(len(chunks))],
            ids=[f"{filename}_{i}" for i in range(len(chunks))]
        )


    return jsonify({"message": "PDF processado com sucesso", "chunks_created": len(chunks)}), 201

# Função para dividir texto em chunks
def chunk_text_recursive(text, chunk_size, chunk_overlap, separators):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    chunks = splitter.split_text(text)
    return chunks

# Busca Semântica
@app.route('/search', methods=['GET'])
@authenticate
def search(role):
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Parâmetro 'query' ausente"}), 400

    # Realiza a busca semântica
    results = semantic_search(query)

    return jsonify(results), 200


# Função de busca semântica
def semantic_search(query):
    query_embedding = embeddings.embed_query(query)
    results = collection.query(query_embedding, n_results=10)

    # Debugging: Print the results structure
    print("Results from query:", results)

    return [
        {
            "document": results["metadatas"][0][i]["document"],  # Acesso correto à metadata
            "chunk": results["metadatas"][0][i]["chunk"],        # Acesso correto ao chunk
            "content": results["documents"][0][i]                 # Acesso correto ao conteúdo do documento
        }
        for i in range(len(results['documents'][0]))  # Loop pelos resultados
    ]




# Exclusão de currículo
@app.route('/curriculum/<id>', methods=['DELETE'])
@authenticate
def delete_curriculum(id, role):
    if not ROLES[role]["delete_curriculum"]:
        return jsonify({"error": "Acesso não autorizado"}), 403
    try:
        collection.delete(ids=[id])
        return jsonify({"message": "Currículo excluído com sucesso"}), 200
    except Exception:
        return jsonify({"error": "Currículo não encontrado"}), 404

# Extração de texto do PDF
def extract_text_from_pdf(pdf_path):
    # Implemente a lógica de extração de texto aqui
    # Exemplo usando PyMuPDF:
    import fitz
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
