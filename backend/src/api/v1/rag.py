from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from ..database import get_db
from ..services.rag_service import RAGService
from ..api.v1.auth import get_current_active_user, User

router = APIRouter()
rag_service = RAGService()

class QueryRequest(BaseModel):
    query: str
    limit: int = 5

class RAGResponse(BaseModel):
    answer: str
    context: List[str]
    references: List[Dict[str, Any]]

@router.post("/query", response_model=RAGResponse)
def query_educational_content(
    request: QueryRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Query the educational content using RAG (Retrieval-Augmented Generation)"""
    try:
        result = rag_service.get_answer_with_context(request.query, request.limit)
        return RAGResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/index")
def index_all_content(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Index all educational content into the vector database"""
    try:
        rag_service.index_educational_content(db)
        return {"message": "Successfully indexed all educational content"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing content: {str(e)}")