import os
import re

import streamlit as st
import chromadb
import fitz
from groq import Groq
from sentence_transformers import SentenceTransformer


def process_pdf(uploaded_file, model, collection, file_name):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_document:
            text = ""
            for page in pdf_document:
                text += page.get_text()
        embeddings = embedding_function(text, model)
        add_document_to_collection(text, embeddings, os.path.basename(file_name), collection)
        print(f"{file_name} processado com sucesso.")
    except Exception as e:
        print(f"Erro ao ler o PDF {file_name}: {str(e)}")


def get_pdfs_from_directory(directory: str) -> list:
    """Obtém a lista de arquivos PDF de um diretório."""
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


def add_document_to_collection(document: str, embeddings: list, file_name: str, collection):
    match = re.search(r'curriculo_(\d+)\.pdf', file_name)
    if match:
        doc_id = match.group(1)

        existing_documents = collection.get(
            ids=[doc_id]
        )
        if existing_documents['documents']:
            print(f"Documento com ID {doc_id} já existe. Ignorando a adição.")
            return
        
        collection.add(
            documents=[document],
            embeddings=[embeddings],
            metadatas=[{"source": file_name}],
            ids=[doc_id]
        )
        print(f"Currículo: {doc_id} adicionado com sucesso.")
    else:
        print(f"Nome do arquivo não corresponde ao formato esperado: {file_name}")


def get_response_from_llama(prompt: str) -> str:
    print("Obtendo resposta do Llama")
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

def embedding_function(document: str, model) -> list:
    embeddings = model.encode(document)
    return embeddings


def retrieve_documents(query: str, collection):
    results = collection.query(
            query_texts=[
                query
            ]
        )
    retrieved_documents = ""
    for documents, metadatas in zip(results['documents'], results['metadatas']):
            for document, metadata in zip(documents, metadatas):
                retrieved_documents += f"Documento: {metadata['source']}\nTexto do Documento: {document}\n\n"
    return retrieved_documents

def format_prompt(retrieved_documents: str, query:str) -> str:
    return f""""
        <context>Você é um assistente de analistas de RH e sua missão é <task>responder perguntas de analistas de RH sobre currículos de candidatos que serão analisados.</task></context>
        <instruction>Com base no(s) currículo(s) abaixo, {query}</instruction> Se for relevante para a pergunta traga o trecho da onde você tirou a informação.
        Se você não souber, não responda, não invente respostas.
        <documents>{retrieved_documents}</documents>
    """

def main():
    persist_directory = "./chroma_data"
    collection_name = "curriculum_db_streamlit"
    chroma_client = chromadb.PersistentClient(path=persist_directory)
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    collection = chroma_client.get_or_create_collection(name="curriculum_db_streamlit")
    st.title("Análise de currículos")

    if st.button("Limpar banco de dados"):
        chroma_client.delete_collection(collection_name)
        collection = chroma_client.get_or_create_collection(name="curriculum_db_streamlit")
        st.success("Banco de dados limpo com sucesso.")

    uploaded_files = st.file_uploader(
        "Insira os currículos para análise:", accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            process_pdf(uploaded_file, model, collection, uploaded_file.name)

    query = st.text_input("Faça uma pergunta sobre os candidatos:")

    if query:
        retrieved_documents = retrieve_documents(query, collection)
        prompt = format_prompt(retrieved_documents, query)
        response = get_response_from_llama(prompt)
        st.write(response)
        

if __name__ == '__main__':
    main()
