from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.nodes.classifier import classify_node
from src.agents.nodes.researcher import research_node
from src.agents.nodes.writer import writer_node
from src.agents.nodes.reviewer import reviewer_node
from src.agents.nodes.router import should_research, should_retry

def build_agent_graph():
    g = StateGraph(AgentState)
    g.add_node("classifier", classify_node)
    g.add_node("researcher", research_node)
    g.add_node("writer", writer_node)
    g.add_node("reviewer", reviewer_node)
    g.set_entry_point("classifier")
    g.add_conditional_edges("classifier", should_research, {"research":"researcher","writer":"writer"})
    g.add_edge("researcher", "writer")
    g.add_edge("writer", "reviewer")
    g.add_conditional_edges("reviewer", should_retry, {"end":END,"retry":"writer"})
    return g.compile()

def run_agent(input_text, task_type="auto"):
    return build_agent_graph().invoke({"input_text":input_text,"task_type":task_type,"messages":[],"classification":None,"research_results":None,"draft":None,"review":None,"final_output":None,"status":"pending","retry_count":0,"total_cost":0.0,"error_log":[]})
