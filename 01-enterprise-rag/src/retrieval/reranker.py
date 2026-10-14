import logging
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_settings

logger = logging.getLogger(__name__)

class LLMReranker:
    PROMPT = ChatPromptTemplate.from_messages([("system", "Rate relevancy 0.0-1.0. ONLY a number."), ("human", "Query: {query}\nDoc: {document}\nScore:")])

    def __init__(self):
        s = get_settings()
        self.chain = self.PROMPT | ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=s.OPENAI_API_KEY)

    def rerank(self, query, docs, top_k=3):
        reranked = []
        for doc, orig in docs:
            try:
                score = max(0.0, min(1.0, float(self.chain.invoke({"query": query, "document": doc.page_content[:500]}).content.strip())))
                reranked.append((doc, orig * 0.4 + score * 0.6))
            except:
                reranked.append((doc, orig))
        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_k]
