from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from src.ai.chatbot import SupportChatbot
router = APIRouter(prefix="/chat", tags=["Chat"])
bot = SupportChatbot()
convos = {}
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    user_id: str = "demo"
class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    should_escalate: bool
    confidence: float
    latency_ms: float
@router.post("/message", response_model=ChatResponse)
async def send(req: ChatRequest):
    cid = req.conversation_id or f"c-{len(convos)+1}"
    if cid not in convos: convos[cid] = []
    convos[cid].append({"role":"user","content":req.message})
    try:
        r = await bot.respond(req.message, convos[cid], req.user_id)
        convos[cid].append({"role":"assistant","content":r["response"]})
        return ChatResponse(response=r["response"],conversation_id=cid,should_escalate=r["should_escalate"],confidence=r["confidence"],latency_ms=r["latency_ms"])
    except Exception as e:
        raise HTTPException(500, detail=str(e))
