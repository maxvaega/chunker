import os
import pandas as pd
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings

def load_markdown(file_path):
  """
  Carica il contenuto di un file Markdown.
  """
  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()
      return content
  except Exception as e:
      print(f"Errore nel caricamento del file: {e}")
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

def save_to_csv(chunks, metadata, output_file='output/output_chunks.csv'):
  """
  Salva i chunk in un file CSV con i relativi metadata.
  """
  data = {
      'filename': [metadata['filename']] * len(chunks),
      'datetime': [metadata['datetime']] * len(chunks),
      'chunk': chunks
  }
  df = pd.DataFrame(data)
  try:
      df.to_csv(output_file, index=False)
      print(f"Chunk salvati con successo in {output_file}")
  except Exception as e:
      print(f"Errore nel salvataggio del CSV: {e}")

def upload_to_pinecone(chunks, metadata, index_name, namespace):
  """
  Carica i chunk su Pinecone.
  """
  load_dotenv()  # Carica le variabili d'ambiente dal file .env
  
  PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
  PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
  
  if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
      print("API Key o Environment di Pinecone non configurati correttamente.")
      return
  
  # Inizializzazione di Pinecone con la nuova sintassi
  pc = Pinecone(api_key=PINECONE_API_KEY)
  
  """
  Environment variables for pinecone instance and index

  """
  index_name='aistruttore'
  namespace='aistruttore1'

  # Verifica se l'indice esiste
  if index_name not in pc.list_indexes().names():
      # Crea l'indice se non esiste
      pc.create_index(
          name=index_name,
          dimension=1536,  # Dimensione per OpenAI embeddings
          metric='cosine',
          spec=ServerlessSpec(
              cloud='aws',
              region='us-east-1'  
          )
      )
  
  # Ottieni l'indice
  index = pc.Index(index_name)
  
  # Per ogni chunk, genera un embedding e caricalo
  embeddings = OpenAIEmbeddings()
  
  vectors = []
  for i, chunk in enumerate(chunks):
      embedding = embeddings.embed_query(chunk)
      vectors.append({
          'id': f"{metadata['filename']}_{i}",
          'values': embedding,
          'metadata': {
              'filename': metadata['filename'],
              'datetime': metadata['datetime'],
              'chunk': chunk
          }
      })
  
  try:
      # Carica i vettori in batch
      index.upsert(vectors=vectors, namespace=namespace)
      print(f"Chunk caricati con successo su Pinecone nell'indice '{index_name}' nel namespace '{namespace}'.")
  except Exception as e:
      print(f"Errore nel caricamento su Pinecone: {e}")

def main():
  # Input da parte dell'utente
  file_path = input("Inserisci il percorso del file Markdown (.md): ").strip()
  
  if not os.path.isfile(file_path):
      print("Il file specificato non esiste.")
      return
  
  content = load_markdown(file_path)
  if content is None:
      return
  
  chunks = split_into_chunks(content)
  
  metadata = {
      'filename': os.path.basename(file_path),
      'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  }
  
  # Chiedi all'utente dove salvare i chunk
  print("\nDove desideri salvare i chunk?")
  print("1. Salva localmente in CSV")
  print("2. Carica su Pinecone")
  print("3. Entrambi")
  
  choice = input("Inserisci il numero della tua scelta (1/2/3): ").strip()
  
  if choice == '1':
      save_to_csv(chunks, metadata)
  elif choice == '2':
      upload_to_pinecone(chunks, metadata)
  elif choice == '3':
      save_to_csv(chunks, metadata)
      upload_to_pinecone(chunks, metadata)
  else:
      print("Scelta non valida. Uscita dal programma.")

if __name__ == "__main__":
  main()