import os
import re

import chromadb
import fitz
from sentence_transformers import SentenceTransformer

def read_pdf(file_path: str) -> str:
    """Lê um documento PDF e retorna o texto contido nele."""
    text = ""
    try:
        document = fitz.open(file_path)

        for page_num in range(len(document)):
            page = document[page_num]
            text += page.get_text()

        document.close()
    except Exception as e:
        print(f"Erro ao ler o PDF {file_path}: {str(e)}")

    return text

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
        collection.add(
            documents=[document],
            embeddings=[embeddings],
            metadatas=[{"source": file_name}],
            ids=[doc_id]
        )
    else:
        print(f"Nome do arquivo não corresponde ao formato esperado: {file_name}")

def interactive_query_loop(collection):
    while True:
        print("Digite sua query de busca:")
        query = input()
        if query.lower() == 'sair':
            break
        results = collection.query(
            query_texts=[
                query
            ],
            n_results=5
        )
        print("\nResultados:")
        for documents, metadatas in zip(results['documents'], results['metadatas']):
            for document, metadata in zip(documents, metadatas):
                print(f"Documento: {metadata['source']}")
                print(f"Trecho: {document[:200]}...")
                print()
        

def embedding_function(document: str, model) -> list:
    embeddings = model.encode(document)
    return embeddings

def process_pdf_directory(pdf_directory: str, collection, model) -> None:
    for pdf_file in pdf_directory:
        pdf_text = read_pdf(pdf_file)
        embeddings = embedding_function(pdf_text, model)
        add_document_to_collection(pdf_text, embeddings, os.path.basename(pdf_file), collection)

def main():
    persist_directory = "./chroma_data"
    chroma_client = chromadb.PersistentClient(path=persist_directory)
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    collection = chroma_client.get_or_create_collection(name="curriculum_db")
    curriculum_directory = os.path.join('./Currículos')


    pdf_files = get_pdfs_from_directory(curriculum_directory)

    process_pdf_directory(pdf_files, collection, model)
    interactive_query_loop(collection)


if __name__ == "__main__":
    main()