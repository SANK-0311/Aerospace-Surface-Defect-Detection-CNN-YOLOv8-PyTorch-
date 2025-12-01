import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.config import settings

def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    
    # Check file extension
    file_ext = file.filename.split(".")[-1].lower()
    allowed_exts = settings.get_allowed_extensions()
    
    if file_ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_exts)}"
        )
    
    # Check file size (if content-length header is present)
    if hasattr(file, 'size') and file.size:
        if file.size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024*1024):.1f}MB"
            )

def save_upload_file(file: UploadFile) -> Path:
    """Save uploaded file with unique name"""
    
    # Generate unique filename
    file_ext = file.filename.split(".")[-1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = settings.UPLOAD_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        
        # Check size after reading
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024*1024):.1f}MB"
            )
        
        buffer.write(content)
    
    return file_path

def cleanup_old_files(directory: Path, max_age_hours: int = 24):
    """Delete files older than specified hours"""
    import time
    
    if not directory.exists():
        return
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for file_path in directory.glob("*"):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")