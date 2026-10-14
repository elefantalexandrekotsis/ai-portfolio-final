from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4o"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_support"
    class Config:
        env_file = ".env"
@lru_cache()
def get_settings():
    return Settings()
