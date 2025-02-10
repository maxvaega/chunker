from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, validator
from typing import List, Optional
from app.main import download_markdown_from_url, split_into_chunks, prepare_chunks_data, save_to_json, upload_to_pinecone
from auth import verify_token
import os
from datetime import datetime

app = FastAPI()

class ProcessMarkdownRequest(BaseModel):
    file_url: str
    upload_options: Optional[List[str]] = ["pinecone"]

    @validator('file_url')
    def validate_file_url(cls, v):
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError('file_url must be a valid URL')
        if not v.endswith(".md"):
            raise ValueError('file_url must point to a Markdown file')
        return v

    @validator('upload_options')
    def validate_upload_options(cls, v):
        valid_options = ["local", "pinecone"]
        if not all(option in valid_options for option in v):
            raise ValueError('upload_options must be a list of "local" and/or "pinecone"')
        return v

@app.post("/process-markdown")
async def process_markdown(request: ProcessMarkdownRequest, authorization: str = Header(None)):
    # Verify JWT token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token di autenticazione mancante o non valido.")
    token = authorization.split(" ")[1]
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Token di autenticazione mancante o non valido.")

    # Download Markdown file
    content = download_markdown_from_url(request.file_url)
    if content is None:
        raise HTTPException(status_code=500, detail="Errore durante il download del file Markdown.")

    # Process Markdown file
    chunks = split_into_chunks(content)
    metadata = {
        'filename': os.path.basename(request.file_url),
        'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    chunks_data, chunk_ids, pinecone_metadata, chunks_text = prepare_chunks_data(chunks, metadata)

    # Save chunks locally if requested
    if "local" in request.upload_options:
        output_file = f"output/{metadata['filename']}_{metadata['datetime']}.json"
        save_to_json(chunks_data, output_file)

    # Upload chunks to Pinecone if requested
    if "pinecone" in request.upload_options:
        upload_to_pinecone(chunk_ids, chunks_text, pinecone_metadata)

    return {
        "message": "File processato e chunk caricati con successo.",
        "chunks": chunks_data
    }