from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4o"
    AZURE_OPENAI_API_VERSION: str = "2024-06-01"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "enterprise_docs"
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "enterprise-rag"
    LANGSMITH_TRACING: bool = True
    APP_NAME: str = "Enterprise RAG System"
    LOG_LEVEL: str = "INFO"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.1
    TOP_K: int = 5
    COST_PER_1K_INPUT_TOKENS: float = 0.005
    COST_PER_1K_OUTPUT_TOKENS: float = 0.015

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
