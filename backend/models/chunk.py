from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ChunkRequest(BaseModel):
    # Add validation for content with min length and max length
    content: str = Field(..., min_length=1, max_length=1000000)
    # Add validation for chunk size with reasonable limits
    max_chunk_size: Optional[int] = Field(default=1000, ge=100, le=10000)

    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty or just whitespace")
        return v.strip()

class ChunkMetadata(BaseModel):
    filename: str
    datetime: str
    title: str

class ChunkRequest(BaseModel):
    content: str
    filename: str

class ChunkResponse(BaseModel):
    id: str
    content: str
    title: str
    size: int
    index: int
    metadata: ChunkMetadata

class ChunkError(BaseModel):
    error: str
    detail: Optional[str] = None

class ChunkResult(BaseModel):
    chunks: List[ChunkResponse]
    total_chunks: int = Field(ge=0)
    original_size: int = Field(ge=0)