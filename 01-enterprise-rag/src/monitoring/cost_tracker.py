import logging
from datetime import datetime
from typing import Optional
import tiktoken
from src.config import get_settings

logger = logging.getLogger(__name__)

class CostTracker:
    def __init__(self):
        self.settings = get_settings()
        self.encoder = tiktoken.encoding_for_model("gpt-4o")
        self.total_cost = 0.0
        self.total_requests = 0
        self.history = []

    def count_tokens(self, text):
        return len(self.encoder.encode(text))

    def estimate_cost(self, input_text, output_text, model=None):
        it, ot = self.count_tokens(input_text), self.count_tokens(output_text)
        cost = (it/1000)*self.settings.COST_PER_1K_INPUT_TOKENS + (ot/1000)*self.settings.COST_PER_1K_OUTPUT_TOKENS
        self.total_cost += cost
        self.total_requests += 1
        self.history.append({"timestamp": datetime.utcnow().isoformat(), "input_tokens": it, "output_tokens": ot, "cost_usd": round(cost,6)})
        return round(cost, 6)

    def get_summary(self):
        return {"total_cost_usd": round(self.total_cost,4), "total_requests": self.total_requests, "avg_cost_per_request": round(self.total_cost/max(self.total_requests,1),6), "history": self.history[-50:]}
