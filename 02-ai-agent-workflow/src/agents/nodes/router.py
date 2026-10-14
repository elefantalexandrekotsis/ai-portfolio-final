def should_research(state):
    return "research" if state.get("classification",{}).get("requires_research",True) else "writer"

def should_retry(state):
    if state.get("review",{}).get("approved",False): return "end"
    return "retry" if state.get("retry_count",0) < 2 else "end"
