import json, logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_settings

logger = logging.getLogger(__name__)

def classify_node(state):
    s = get_settings()
    prompt = ChatPromptTemplate.from_messages([("system","Classify. JSON: {{\"task_type\":\"cv_analysis|report_generation|email_draft|general_query\",\"complexity\":\"low|medium|high\",\"requires_research\":true/false}}"),("human","{input_text}")])
    try:
        c = json.loads((prompt | ChatOpenAI(model="gpt-4o-mini",temperature=0,api_key=s.OPENAI_API_KEY)).invoke({"input_text":state["input_text"]}).content)
        return {**state, "classification":c, "task_type":c["task_type"], "status":"processing"}
    except Exception as e:
        return {**state, "classification":{"task_type":"general_query"}, "task_type":"general_query", "status":"processing", "error_log":state.get("error_log",[])+[str(e)]}
