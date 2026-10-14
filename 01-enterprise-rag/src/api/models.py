from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    category: Optional[str] = None
    use_reranker: bool = True

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    metadata: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    version: str
    vector_db: str
    documents_count: int

class IngestRequest(BaseModel):
    data_dir: str = "data/raw"
    chunk_size: int = Field(512, ge=100, le=2000)
    chunk_overlap: int = Field(50, ge=0, le=200)

class IngestResponse(BaseModel):
    documents_loaded: int
    chunks_created: int
    vectors_stored: int

class CostSummaryResponse(BaseModel):
    total_cost_usd: float
    total_requests: int
    avg_cost_per_request: float
    history: List[Dict[str, Any]]
