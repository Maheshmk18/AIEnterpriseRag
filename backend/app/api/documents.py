import os
import shutil
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..core.deps import get_db, get_current_user, get_current_admin_user
from ..database.models import User, Document
from ..services.document_processor import document_processor
from ..services.rag_pipeline import rag_pipeline

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    chunk_count: int
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Only admin can upload
):
    """Upload a document to the knowledge base. Admin only."""
    file_ext = get_file_extension(file.filename)
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = os.path.getsize(file_path)
    
    document = Document(
        filename=unique_filename,
        original_filename=file.filename,
        file_type=file_ext,
        file_size=file_size,
        status="processing",
        owner_id=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    try:
        chunks, content_hash = document_processor.process_document(file_path, file_ext)
        
        # Index document
        chunk_count = rag_pipeline.index_document(
            document_id=document.id,
            chunks=chunks,
            filename=file.filename,
            user_id=current_user.id
        )
        
        document.content_hash = content_hash
        document.chunk_count = chunk_count
        document.status = "processed"
        db.commit()
        db.refresh(document)
        
    except Exception as e:
        document.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )
    
    return document


@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all documents. All users can see all documents."""
    documents = db.query(Document).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific document."""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Only admin can delete
):
    """Delete a document. Admin only."""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete from vector store
    try:
        rag_pipeline.delete_document(document_id)
    except Exception as e:
        print(f"Error deleting from vector store: {e}")
    
    # Delete file
    file_path = os.path.join(UPLOAD_DIR, document.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
