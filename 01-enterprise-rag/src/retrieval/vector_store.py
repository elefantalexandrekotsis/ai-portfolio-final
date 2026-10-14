import logging
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from src.config import get_settings

logger = logging.getLogger(__name__)

class VectorRetriever:
    def __init__(self):
        self.settings = get_settings()
        if self.settings.AZURE_OPENAI_API_KEY:
            self.embeddings = AzureOpenAIEmbeddings(azure_endpoint=self.settings.AZURE_OPENAI_ENDPOINT, api_key=self.settings.AZURE_OPENAI_API_KEY, model=self.settings.EMBEDDING_MODEL)
        else:
            self.embeddings = OpenAIEmbeddings(model=self.settings.EMBEDDING_MODEL, api_key=self.settings.OPENAI_API_KEY)
        self.qdrant = QdrantClient(url=self.settings.QDRANT_URL)

    def retrieve(self, query, top_k=None, category_filter=None, score_threshold=0.7):
        top_k = top_k or self.settings.TOP_K
        qv = self.embeddings.embed_query(query)
        qf = Filter(must=[FieldCondition(key="metadata.category", match=MatchValue(value=category_filter))]) if category_filter else None
        results = self.qdrant.search(collection_name=self.settings.QDRANT_COLLECTION, query_vector=qv, limit=top_k, query_filter=qf, score_threshold=score_threshold)
        docs = [(Document(page_content=r.payload["text"], metadata={**r.payload.get("metadata", {}), "relevance_score": r.score}), r.score) for r in results]
        logger.info(f"Retrieved {len(docs)} docs")
        return docs
