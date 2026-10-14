import json, logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_settings

logger = logging.getLogger(__name__)

def research_node(state):
    s = get_settings()
    prompt = ChatPromptTemplate.from_messages([("system","Extract info. JSON: {{\"findings\":[{{\"topic\":\"...\",\"details\":\"...\"}}],\"key_insights\":[\"...\"]}}"),("human","Input: {input_text}\nClass: {classification}")])
    try:
        r = json.loads((prompt | ChatOpenAI(model="gpt-4o",temperature=0.1,api_key=s.OPENAI_API_KEY)).invoke({"input_text":state["input_text"],"classification":str(state.get("classification",{}))}).content)
        return {**state, "research_results": r.get("findings",[])}
    except Exception as e:
        return {**state, "research_results":[], "error_log":state.get("error_log",[])+[str(e)]}
