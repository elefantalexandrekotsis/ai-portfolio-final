import os
from src.config import get_settings

def setup_langsmith():
    s = get_settings()
    if s.LANGSMITH_TRACING and s.LANGSMITH_API_KEY:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = s.LANGSMITH_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = s.LANGSMITH_PROJECT
