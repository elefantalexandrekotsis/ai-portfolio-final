import logging, uuid
from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from src.config import get_settings

logger = logging.getLogger(__name__)

class DocumentEmbedder:
    def __init__(self):
        self.settings = get_settings()
        if self.settings.AZURE_OPENAI_API_KEY:
            self.embeddings = AzureOpenAIEmbeddings(azure_endpoint=self.settings.AZURE_OPENAI_ENDPOINT, api_key=self.settings.AZURE_OPENAI_API_KEY, model=self.settings.EMBEDDING_MODEL)
        else:
            self.embeddings = OpenAIEmbeddings(model=self.settings.EMBEDDING_MODEL, api_key=self.settings.OPENAI_API_KEY)
        self.qdrant = QdrantClient(url=self.settings.QDRANT_URL)
        self._ensure_collection()

    def _ensure_collection(self):
        names = [c.name for c in self.qdrant.get_collections().collections]
        if self.settings.QDRANT_COLLECTION not in names:
            self.qdrant.create_collection(collection_name=self.settings.QDRANT_COLLECTION, vectors_config=VectorParams(size=self.settings.EMBEDDING_DIMENSIONS, distance=Distance.COSINE))

    def embed_and_store(self, chunks, batch_size=100):
        total = 0
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            vectors = self.embeddings.embed_documents([c.page_content for c in batch])
            points = [PointStruct(id=str(uuid.uuid4()), vector=v, payload={"text": c.page_content, "metadata": c.metadata}) for c, v in zip(batch, vectors)]
            self.qdrant.upsert(collection_name=self.settings.QDRANT_COLLECTION, points=points)
            total += len(points)
        logger.info(f"Stored {total} vectors")
        return total
