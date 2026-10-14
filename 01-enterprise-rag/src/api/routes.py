import logging
from fastapi import APIRouter, HTTPException
from src.api.models import QueryRequest, QueryResponse, HealthResponse, IngestRequest, IngestResponse, CostSummaryResponse
from src.generation.chain import RAGChain
from src.generation.guardrails import InputGuardrail
from src.ingestion.loader import DocumentLoader
from src.ingestion.chunker import DocumentChunker
from src.ingestion.embedder import DocumentEmbedder

logger = logging.getLogger(__name__)
router = APIRouter()
_chain = None
_guard = None

def get_chain():
    global _chain
    if not _chain: _chain = RAGChain()
    return _chain

def get_guard():
    global _guard
    if not _guard: _guard = InputGuardrail()
    return _guard

@router.get("/health", response_model=HealthResponse)
async def health():
    try:
        from qdrant_client import QdrantClient
        from src.config import get_settings
        s = get_settings()
        col = QdrantClient(url=s.QDRANT_URL).get_collection(s.QDRANT_COLLECTION)
        return HealthResponse(status="healthy", version="1.0.0", vector_db="connected", documents_count=col.points_count)
    except:
        return HealthResponse(status="degraded", version="1.0.0", vector_db="disconnected", documents_count=0)

@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    v = get_guard().validate(req.question)
    if not v.get("safe", True):
        raise HTTPException(400, detail={"error": "Blocked", "reason": v.get("reason")})
    try:
        return QueryResponse(**get_chain().invoke(question=req.question, category_filter=req.category))
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/ingest", response_model=IngestResponse)
async def ingest(req: IngestRequest):
    try:
        docs = DocumentLoader(req.data_dir).load_all()
        chunks = DocumentChunker(req.chunk_size, req.chunk_overlap).chunk(docs)
        stored = DocumentEmbedder().embed_and_store(chunks)
        return IngestResponse(documents_loaded=len(docs), chunks_created=len(chunks), vectors_stored=stored)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.get("/costs", response_model=CostSummaryResponse)
async def costs():
    return CostSummaryResponse(**get_chain().cost_tracker.get_summary())
