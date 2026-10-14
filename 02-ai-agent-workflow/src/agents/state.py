from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    input_text: str
    task_type: str
    messages: Annotated[list, add_messages]
    classification: Optional[dict]
    research_results: Optional[List[dict]]
    draft: Optional[str]
    review: Optional[dict]
    final_output: Optional[str]
    status: str
    retry_count: int
    total_cost: float
    error_log: List[str]
