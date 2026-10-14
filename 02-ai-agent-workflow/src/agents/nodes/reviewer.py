import json, logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_settings

logger = logging.getLogger(__name__)

def reviewer_node(state):
    s = get_settings()
    prompt = ChatPromptTemplate.from_messages([("system","Review. JSON: {{\"quality_score\":0.0-1.0,\"approved\":true/false,\"revised_output\":\"..or null\"}}"),("human","Task:{task_type}\nRequest:{input_text}\nDraft:\n{draft}")])
    try:
        rev = json.loads((prompt | ChatOpenAI(model="gpt-4o",temperature=0,api_key=s.OPENAI_API_KEY)).invoke({"task_type":state.get("task_type",""),"input_text":state["input_text"],"draft":state.get("draft","")}).content)
        final = state.get("draft","") if rev.get("approved") else (rev.get("revised_output") or state.get("draft",""))
        return {**state, "review":rev, "final_output":final, "status":"completed"}
    except Exception as e:
        return {**state, "final_output":state.get("draft",""), "status":"completed", "error_log":state.get("error_log",[])+[str(e)]}
