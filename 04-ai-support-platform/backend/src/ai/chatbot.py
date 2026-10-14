import time
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from src.config import get_settings
from src.ai.prompts import SUPPORT_SYSTEM_PROMPT
from src.ai.escalation import EscalationDetector
class SupportChatbot:
    def __init__(self):
        s = get_settings()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2, max_tokens=500, api_key=s.OPENAI_API_KEY)
        self.escalation = EscalationDetector()
        self.prompt = ChatPromptTemplate.from_messages([("system",SUPPORT_SYSTEM_PROMPT),MessagesPlaceholder("history"),("human","{input}")])
    async def respond(self, user_message, history, user_id):
        t = time.time()
        esc = self.escalation.check(user_message, history)
        if esc["should_escalate"]:
            return {"response":esc["escalation_message"],"should_escalate":True,"confidence":1.0,"sources":[],"latency_ms":(time.time()-t)*1000,"cost":0}
        msgs = [HumanMessage(content=m["content"]) if m["role"]=="user" else AIMessage(content=m["content"]) for m in history[-10:]]
        r = await (self.prompt | self.llm).ainvoke({"history":msgs,"input":user_message})
        return {"response":r.content,"should_escalate":False,"confidence":0.85,"sources":[],"latency_ms":(time.time()-t)*1000,"cost":0.005}
