from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
import logging
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models.chunk import ChunkRequest, ChunkResponse, ChunkMetadata
from utils.auth import verify_token
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def extract_title(chunk: str) -> str:
    """Extracts title from markdown chunk."""
    first_line = chunk.strip().split('\n')[0]
    return re.sub(r'^#+\s*', '', first_line).strip()

@router.post("/process", response_model=List[ChunkResponse])
async def process_chunks(
    request: ChunkRequest,
    token: str = Depends(oauth2_scheme)
):
    try:
        verify_token(token)
        
        # Use same splitter configuration as main.py
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=0,
            separators=['##'],
            keep_separator=True
        )
        
        # Split text into chunks
        chunks = splitter.split_text(request.content)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create ChunkResponse objects
        responses = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{request.filename}_{str(i+1).zfill(3)}"
            title = extract_title(chunk)
            
            metadata = ChunkMetadata(
                filename=request.filename,
                datetime=current_time,
                title=title
            )
            
            response = ChunkResponse(
                id=chunk_id,
                content=chunk,
                title=title,
                size=len(chunk),
                index=i,
                metadata=metadata
            )
            responses.append(response)
        
        logger.info(f"Successfully processed {len(chunks)} chunks")
        return responses
        
    except Exception as e:
        logger.error(f"Error processing chunks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))