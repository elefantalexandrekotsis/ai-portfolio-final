import logging, time
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config import get_settings
from src.generation.prompts import SYSTEM_PROMPT, RAG_PROMPT
from src.retrieval.vector_store import VectorRetriever
from src.retrieval.reranker import LLMReranker
from src.monitoring.cost_tracker import CostTracker

logger = logging.getLogger(__name__)

class RAGChain:
    def __init__(self, use_reranker=True):
        self.settings = get_settings()
        self.retriever = VectorRetriever()
        self.reranker = LLMReranker() if use_reranker else None
        self.cost_tracker = CostTracker()
        if self.settings.AZURE_OPENAI_API_KEY:
            self.llm = AzureChatOpenAI(azure_endpoint=self.settings.AZURE_OPENAI_ENDPOINT, api_key=self.settings.AZURE_OPENAI_API_KEY, azure_deployment=self.settings.AZURE_OPENAI_DEPLOYMENT, api_version=self.settings.AZURE_OPENAI_API_VERSION, temperature=self.settings.TEMPERATURE, max_tokens=self.settings.MAX_TOKENS)
        else:
            self.llm = ChatOpenAI(model="gpt-4o", temperature=self.settings.TEMPERATURE, max_tokens=self.settings.MAX_TOKENS, api_key=self.settings.OPENAI_API_KEY)
        self.prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", RAG_PROMPT)])

    def invoke(self, question, category_filter=None):
        t = time.time()
        docs = self.retriever.retrieve(query=question, category_filter=category_filter)
        if not docs:
            return {"answer": "No relevant documents found.", "sources": [], "metadata": {"retrieval_count": 0, "latency_ms": (time.time()-t)*1000}}
        if self.reranker:
            docs = self.reranker.rerank(question, docs)
        ctx = "\n\n---\n\n".join(f"[Doc {i}] (source: {d.metadata.get('source_file','?')}, score: {s:.2f})\n{d.page_content}" for i,(d,s) in enumerate(docs,1))
        resp = (self.prompt | self.llm | StrOutputParser()).invoke({"context": ctx, "question": question})
        lat = (time.time()-t)*1000
        sources = list(set(d.metadata.get("source_file","?") for d,_ in docs))
        cost = self.cost_tracker.estimate_cost(ctx+question, resp)
        return {"answer": resp, "sources": sources, "metadata": {"retrieval_count": len(docs), "latency_ms": round(lat,2), "estimated_cost_usd": cost, "model": self.settings.AZURE_OPENAI_DEPLOYMENT or "gpt-4o"}}
