import os
import json
from datetime import datetime
from dotenv import load_dotenv
import re
import requests
from urllib.parse import urlparse

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from app.api import app as api_app

def load_key():
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
    os.environ["LANGCHAIN_PROJECT"] = os.getenv('LANGCHAIN_PROJECT')

def extract_title(chunk):
    """
    Estrae il titolo da un chunk Markdown.
    Il titolo è previsto nella prima riga, preceduto da caratteri #.
    """
    first_line = chunk.strip().split('\n')[0]
    title = re.sub(r'^#+\s*', '', first_line).strip()
    return title

def load_markdown(file_path):
    """
    Carica il contenuto di un file Markdown.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Errore caricando il file: {e}")
        return None

def split_into_chunks(text, separator='##'):
    """
    Suddivide il testo in chunk ogni volta che trova il separatore specificato.
    Mantiene il separatore all'inizio di ogni chunk.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=0,
        separators=[separator],
        keep_separator=True
    )
    chunks = splitter.split_text(text)
    return chunks

def prepare_chunks_data(chunks, metadata):
    """
    Prepara i dati dei chunk con i metadati per il salvataggio.
    Restituisce una tupla contenente:
    1. Lista di dizionari con i dati completi dei chunk
    2. Lista di ID dei chunk
    3. Lista di dizionari dei metadati per Pinecone
    4. Lista di testi dei chunk
    """
    chunk_ids = [f"{metadata['filename']}_{str(i+1).zfill(3)}" for i in range(len(chunks))]
    chunk_titles = [extract_title(chunk) for chunk in chunks]
    
    # Prepara i dati completi dei chunk per il salvataggio in JSON
    chunks_data = []
    # Prepara la lista dei metadati per Pinecone
    pinecone_metadata = []
    
    for chunk_id, title, text in zip(chunk_ids, chunk_titles, chunks):
        # Dati completi del chunk per il salvataggio in JSON
        chunk_data = {
            'id': chunk_id,
            'filename': metadata['filename'],
            'datetime': metadata['datetime'],
            'title': title,
            'text': text
        }
        chunks_data.append(chunk_data)
        
        # Metadati per Pinecone
        pinecone_metadata.append({
            'filename': metadata['filename'],
            'datetime': metadata['datetime'],
            'title': title
        })
    
    return chunks_data, chunk_ids, pinecone_metadata, chunks

def save_to_json(chunks_data, output_file='output/output_chunks.json'):
    """
    Salva i chunk in un file JSON con i metadati correlati.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks_data, f, ensure_ascii=False, indent=2)
        print(f"Chunk salvati con successo in {output_file}")
    except Exception as e:
        print(f"Errore salvando il JSON: {e}")

def upload_to_pinecone(chunk_ids, chunks, metadatas):
    """
    Carica i chunk su Pinecone utilizzando LangChain's Pinecone VectorStore.
    """
    load_dotenv()

    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')

    if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
        print("Chiave API o Ambiente Pinecone non configurati correttamente.")
        return

    try:
        index_name = 'aistruttore'
        namespace = 'aistruttore1'

        # Inizializza gli embeddings
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        # Carica i dati utilizzando LangChain's Pinecone VectorStore
        vectorstore = PineconeVectorStore.from_texts(
            texts=chunks,
            embedding=embeddings,
            index_name=index_name,
            namespace=namespace,
            metadatas=metadatas,
            ids=chunk_ids,
            text_key="text"
        )
        print(f"Chunk caricati con successo su Pinecone nell'indice '{index_name}' e namespace '{namespace}'.")
    except Exception as e:
        print(f"Errore caricando su Pinecone: {e}")

def is_url(path):
    """
    Controlla se il percorso fornito è un URL.
    """
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_markdown_from_url(url):
    """
    Scarica il contenuto Markdown da un URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Errore scaricando dall'URL: {e}")
        return None
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api_app, host="0.0.0.0", port=8000)