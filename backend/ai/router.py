from fastapi import APIRouter, Query, Depends
from .service import get_rag_chatbot_service
from backend.data.service import SalesRepService

router = APIRouter()


@router.get("/")
async def ask_question(q: str = Query(..., description="question for the RAG chatbot"), rag_chatbot_service=Depends(get_rag_chatbot_service)):
    """
    Returns AI responses.
    """
    # Placeholder logic: replace with actual AI model call
    resp = await rag_chatbot_service.query(q)
    return resp
