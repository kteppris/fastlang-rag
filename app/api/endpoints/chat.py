from fastapi import APIRouter, Depends, HTTPException, Body
from langchain.chains.base import Chain
from langchain.vectorstores.base import VectorStore

from api.dependencies import get_chain

router = APIRouter()

@router.post("/chat/")
async def get_answer(question: str = Body(...), chain: Chain = Depends(get_chain)):
    try:
        # Get answer from the qa_chain
        answer = chain(question)
        
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {e}")
