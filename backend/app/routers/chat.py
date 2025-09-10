# backend/app/routers/chat.py
from fastapi import APIRouter
from ..models.employee import ChatRequest, ChatResponse, EmployeeSearchResult
from ..services.rag_service import RAGService

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):
    rag = RAGService.instance()
    result = rag.generate(req.query, top_k=req.top_k)
    # map candidates to EmployeeSearchResult models
    candidates = []
    for c in result.get("candidates", []):
        candidates.append(
            EmployeeSearchResult(employee=c["employee"], score=c["score"])
        )
    return {"answer": result["answer"], "candidates": candidates}
