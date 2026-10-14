from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "ai-agent-workflow"
    LOG_LEVEL: str = "INFO"
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
