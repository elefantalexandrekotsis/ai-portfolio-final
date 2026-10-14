import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import get_settings

logger = logging.getLogger(__name__)

def writer_node(state):
    s = get_settings()
    prompt = ChatPromptTemplate.from_messages([("system","Professional writer."),("human","Write based on research.\nResearch: {research}\nInput: {input_text}")])
    try:
        r = (prompt | ChatOpenAI(model="gpt-4o",temperature=0.3,api_key=s.OPENAI_API_KEY)).invoke({"research":str(state.get("research_results",[])),"input_text":state["input_text"]})
        return {**state, "draft": r.content}
    except Exception as e:
        return {**state, "draft":f"Error: {e}", "error_log":state.get("error_log",[])+[str(e)]}
