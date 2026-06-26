from app.graph.state import CrisisState
from retriever import retrieve_context

def rag_agent(state: CrisisState):
    description = state.get("crisis_description", "")
    context = retrieve_context(description, top_k=3)
    return {
        "rag_context": context
    }