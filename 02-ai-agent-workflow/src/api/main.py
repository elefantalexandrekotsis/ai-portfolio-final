import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from src.agents.graph import run_agent

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="AI Agent Workflow", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AgentRequest(BaseModel):
    input_text: str = Field(..., min_length=10)
    task_type: str = "auto"

class AgentResponse(BaseModel):
    final_output: str
    status: str
    task_type: str
    quality_score: Optional[float] = None
    errors: list = []

@app.post("/api/v1/run", response_model=AgentResponse)
async def run(req: AgentRequest):
    try:
        r = run_agent(req.input_text, req.task_type)
        rev = r.get("review",{}) or {}
        return AgentResponse(final_output=r.get("final_output",""), status=r.get("status","?"), task_type=r.get("task_type","?"), quality_score=rev.get("quality_score"), errors=r.get("error_log",[]))
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.get("/api/v1/health")
async def health():
    return {"status":"healthy"}
