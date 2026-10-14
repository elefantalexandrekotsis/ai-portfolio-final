import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.chat import router as chat_router
from src.api.routes.analytics import router as analytics_router
logging.basicConfig(level=logging.INFO)
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
app = FastAPI(title="AI Support Platform", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(chat_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
@app.get("/api/v1/health")
async def health():
    return {"status":"healthy"}
