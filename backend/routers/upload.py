from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Configure upload settings
UPLOAD_DIR = Path("uploads")
# ALLOWED_EXTENSIONS = {".txt", ".pdf", ".doc", ".docx", ".md"}
ALLOWED_EXTENSIONS = {".md"}

# Create uploads directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a single file
    """
    try:
        # Validate file extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}"
            )

        # Create safe filename
        safe_filename = Path(file.filename).stem + file_extension
        file_path = UPLOAD_DIR / safe_filename

        # Save the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"File uploaded successfully: {safe_filename}")
        return {
            "filename": safe_filename,
            "size": len(content),
            "content_type": file.content_type
        }

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.post("/multiple", status_code=201)
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple files
    """
    try:
        results = []
        for file in files:
            # Validate file extension
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                continue

            # Create safe filename
            safe_filename = Path(file.filename).stem + file_extension
            file_path = UPLOAD_DIR / safe_filename

            # Save the file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            results.append({
                "filename": safe_filename,
                "size": len(content),
                "content_type": file.content_type
            })

        logger.info(f"Multiple files uploaded successfully: {len(results)} files")
        return results

    except Exception as e:
        logger.error(f"Error uploading multiple files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

@router.get("/files")
async def list_files():
    """
    List all uploaded files
    """
    try:
        files = []
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "created_at": file_path.stat().st_ctime
                })
        return files

    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")