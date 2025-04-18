from fastapi import APIRouter, Query, Depends
from .service import get_rag_chatbot_service
from backend.data.service import SalesRepService
from .schemas import QueryRequest, QueryResponse
router = APIRouter()


@router.post("/")
async def ask_question(q: QueryRequest, rag_chatbot_service=Depends(get_rag_chatbot_service)):
    """
    Returns AI responses.
    """
    resp = await rag_chatbot_service.query(q.message)
    resp = QueryResponse(**resp)
    return resp
