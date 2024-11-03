import os
import pandas as pd
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings

def load_markdown(file_path):
  """
  Loads the content of a Markdown file.
  """
  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()
      return content
  except Exception as e:
      print(f"Error loading file: {e}")
      return None

def split_into_chunks(text, separator='##'):
  """
  Splits the text into chunks whenever it finds the specified separator.
  Keeps the separator at the beginning of each chunk.
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
  Saves chunks to a CSV file with related metadata.
  """
  data = {
      'filename': [metadata['filename']] * len(chunks),
      'datetime': [metadata['datetime']] * len(chunks),
      'chunk': chunks
  }
  df = pd.DataFrame(data)
  try:
      df.to_csv(output_file, index=False)
      print(f"Chunks successfully saved to {output_file}")
  except Exception as e:
      print(f"Error saving CSV: {e}")

def upload_to_pinecone(chunks, metadata, index_name, namespace):
  """
  Uploads chunks to Pinecone.
  """
  load_dotenv()  # Load environment variables from .env file
  
  PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
  PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
  
  if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
      print("Pinecone API Key or Environment not properly configured.")
      return
  
  # Initialize Pinecone with new syntax
  pc = Pinecone(api_key=PINECONE_API_KEY)
  
  """
  Environment variables for pinecone instance and index
  """
  index_name='aistruttore'
  namespace='aistruttore1'

  # Check if index exists
  if index_name not in pc.list_indexes().names():
      # Create index if it doesn't exist
      pc.create_index(
          name=index_name,
          dimension=1536,  # Dimension for OpenAI embeddings
          metric='cosine',
          spec=ServerlessSpec(
              cloud='aws',
              region='us-east-1'  
          )
      )
  
  # Get the index
  index = pc.Index(index_name)
  
  # Generate embedding and upload for each chunk
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
      # Upload vectors in batch
      index.upsert(vectors=vectors, namespace=namespace)
      print(f"Chunks successfully uploaded to Pinecone in index '{index_name}' and namespace '{namespace}'.")
  except Exception as e:
      print(f"Error uploading to Pinecone: {e}")

def main():
  # User input
  file_path = input("Enter the path to the Markdown file (.md): ").strip()
  
  if not os.path.isfile(file_path):
      print("The specified file does not exist.")
      return
  
  content = load_markdown(file_path)
  if content is None:
      return
  
  chunks = split_into_chunks(content)
  
  metadata = {
      'filename': os.path.basename(file_path),
      'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  }
  
  # Ask user where to save the chunks
  print("\nWhere do you want to save the chunks?")
  print("1. Save locally to CSV")
  print("2. Upload to Pinecone")
  print("3. Both")
  
  choice = input("Enter your choice (1/2/3): ").strip()
  
  if choice == '1':
      save_to_csv(chunks, metadata)
  elif choice == '2':
      upload_to_pinecone(chunks, metadata)
  elif choice == '3':
      save_to_csv(chunks, metadata)
      upload_to_pinecone(chunks, metadata)
  else:
      print("Invalid choice. Exiting program.")

if __name__ == "__main__":
  main()