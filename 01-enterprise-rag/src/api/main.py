import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.api.routes import router
from src.api.middleware import RequestLoggingMiddleware
from src.monitoring.langsmith_config import setup_langsmith

settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL), format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_langsmith()
    yield

app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(RequestLoggingMiddleware)
app.include_router(router, prefix="/api/v1")
