import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import re

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def load_key():
    load_dotenv()  # Load environment variables from .env file
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
    os.environ["LANGCHAIN_PROJECT"] = os.getenv('LANGCHAIN_PROJECT')

def extract_title(chunk):
    """
    Extracts the title from a markdown chunk.
    The title is expected to be in the first line, preceded by # characters.
    """
    # Get the first line of the chunk
    first_line = chunk.strip().split('\n')[0]
    
    # Remove all # characters from the start and any leading/trailing whitespace
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

def save_to_csv(chunks, metadata, output_file='output/output_chunks.csv'):
    """
    Saves chunks to a CSV file with related metadata.
    """
    # Generate chunk IDs and extract titles
    chunk_ids = [f"{metadata['filename']}_{str(i+1).zfill(3)}" for i in range(len(chunks))]
    chunk_titles = [extract_title(chunk) for chunk in chunks]

    data = {
        'id': chunk_ids,
        'filename': [metadata['filename']] * len(chunks),
        'datetime': [metadata['datetime']] * len(chunks),
        'title': chunk_titles,
        'text': chunks
    }
    df = pd.DataFrame(data)
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"Chunks successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving CSV: {e}")

def upload_to_pinecone(chunks, metadata):
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
        namespace = 'aistruttore3'

        # Initialize embeddings
        embeddings = OpenAIEmbeddings()

        # Generate chunk IDs and extract titles
        chunk_ids = [f"{metadata['filename']}_{str(i+1).zfill(3)}" for i in range(len(chunks))]
        chunk_titles = [extract_title(chunk) for chunk in chunks]

        # Prepare metadata for each chunk
        metadatas = [
            {
                'filename': metadata['filename'],
                'datetime': metadata['datetime'],
                'title': title
            }
            for title in chunk_titles
        ]

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
    filename = os.path.basename(file_path)
    print(f"\nCreated {len(chunks)} chunks from file '{filename}'")

    # Print extracted titles for verification
    print("\nExtracted titles:")
    for i, chunk in enumerate(chunks, 1):
        title = extract_title(chunk)
        print(f"Chunk {i}: {title}")

    # Ask user where to save the chunks
    print("\nWhere do you want to save the chunks?")
    print("1. Save locally to CSV")
    print("2. Upload to Pinecone")
    print("3. Both")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == '1':
        output_file=f"output/{filename}_{datetime.now().strftime("%Y-%m-%d %H:%M")}.csv"
        save_to_csv(chunks, metadata, output_file)
    elif choice == '2':
        upload_to_pinecone(chunks, metadata)
    elif choice == '3':
        output_file=f"output/{filename}_{datetime.now().strftime("%Y-%m-%d %H:%M")}.csv"
        save_to_csv(chunks, metadata, output_file)
        upload_to_pinecone(chunks, metadata)
    else:
        print("Invalid choice. Exiting program.")

if __name__ == "__main__":
    main()