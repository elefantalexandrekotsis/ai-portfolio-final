import json, logging
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_settings
from src.generation.prompts import GUARDRAIL_PROMPT

logger = logging.getLogger(__name__)

class InputGuardrail:
    BLOCKED = ["ignore previous", "ignore all instructions", "system prompt", "you are now", "pretend you are", "reveal your instructions"]

    def __init__(self):
        s = get_settings()
        self.chain = ChatPromptTemplate.from_messages([("human", GUARDRAIL_PROMPT)]) | ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=s.OPENAI_API_KEY)

    def validate(self, query):
        for p in self.BLOCKED:
            if p in query.lower():
                return {"safe": False, "reason": f"Blocked: {p}", "category": "injection"}
        try:
            return json.loads(self.chain.invoke({"query": query}).content)
        except:
            return {"safe": True, "reason": "Check failed", "category": "error"}
