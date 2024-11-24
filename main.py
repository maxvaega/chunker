import os
import json
from datetime import datetime
from dotenv import load_dotenv
import re

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def load_key():
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
    os.environ["LANGCHAIN_PROJECT"] = os.getenv('LANGCHAIN_PROJECT')

def extract_title(chunk):
    """
    Extracts the title from a markdown chunk.
    The title is expected to be in the first line, preceded by # characters.
    """
    first_line = chunk.strip().split('\n')[0]
    title = re.sub(r'^#+\s*', '', first_line).strip()
    return title

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

def prepare_chunks_data(chunks, metadata):
    """
    Prepares chunks data with metadata for saving.
    Returns a tuple containing:
    1. List of dictionaries with full chunk data
    2. List of chunk IDs
    3. List of metadata dictionaries for Pinecone
    4. List of text chunks
    """
    chunk_ids = [f"{metadata['filename']}_{str(i+1).zfill(3)}" for i in range(len(chunks))]
    chunk_titles = [extract_title(chunk) for chunk in chunks]
    
    # Prepare full chunk data for JSON storage
    chunks_data = []
    # Prepare metadata list for Pinecone
    pinecone_metadata = []
    
    for chunk_id, title, text in zip(chunk_ids, chunk_titles, chunks):
        # Full chunk data for JSON
        chunk_data = {
            'id': chunk_id,
            'filename': metadata['filename'],
            'datetime': metadata['datetime'],
            'title': title,
            'text': text
        }
        chunks_data.append(chunk_data)
        
        # Metadata for Pinecone
        pinecone_metadata.append({
            'filename': metadata['filename'],
            'datetime': metadata['datetime'],
            'title': title
        })
    
    return chunks_data, chunk_ids, pinecone_metadata, chunks

def save_to_json(chunks_data, output_file='output/output_chunks.json'):
    """
    Saves chunks to a JSON file with related metadata.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks_data, f, ensure_ascii=False, indent=2)
        print(f"Chunks successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving JSON: {e}")

def upload_to_pinecone(chunk_ids, chunks, metadatas):
    """
    Uploads chunks to Pinecone using LangChain's Pinecone VectorStore.
    """
    load_dotenv()

    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')

    if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
        print("Pinecone API Key or Environment not properly configured.")
        return

    try:
        index_name = 'aistruttore'
        namespace = 'aistruttore5'

        # Initialize embeddings
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        # Upload data using LangChain's Pinecone VectorStore
        vectorstore = PineconeVectorStore.from_texts(
            texts=chunks,
            embedding=embeddings,
            index_name=index_name,
            namespace=namespace,
            metadatas=metadatas,
            ids=chunk_ids,
            text_key="text"
        )
        print(f"Chunks successfully uploaded to Pinecone in index '{index_name}' and namespace '{namespace}'.")
    except Exception as e:
        print(f"Error uploading to Pinecone: {e}")

def main():
    # User input
    file_path = input("Enter the path to the Markdown file (.md): ").strip("'", )

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
    filename = os.path.basename(file_path)
    print(f"\nCreated {len(chunks)} chunks from file '{filename}'")

    # Print extracted titles for verification
    print("\nExtracted titles:")
    for i, chunk in enumerate(chunks, 1):
        title = extract_title(chunk)
        print(f"Chunk {i}: {title}")

    # Ask user where to save the chunks
    print("\nWhere do you want to save the chunks?")
    print("1. Save locally to JSON")
    print("2. Upload to Pinecone")
    print("3. Both")

    choice = input("Enter your choice (1/2/3): ").strip()

    # Prepare chunks data for all cases
    chunks_data, chunk_ids, pinecone_metadata, chunks_text = prepare_chunks_data(chunks, metadata)
    
    if choice == '1':
        output_file = f"output/{filename}_{datetime.now().strftime('%Y-%m-%d %H:%M')}.json"
        save_to_json(chunks_data, output_file)
    elif choice == '2':
        upload_to_pinecone(chunk_ids, chunks_text, pinecone_metadata)
    elif choice == '3':
        output_file = f"output/{filename}_{datetime.now().strftime('%Y-%m-%d %H:%M')}.json"
        save_to_json(chunks_data, output_file)
        upload_to_pinecone(chunk_ids, chunks_text, pinecone_metadata)
    else:
        print("Invalid choice. Exiting program.")

if __name__ == "__main__":
    main()