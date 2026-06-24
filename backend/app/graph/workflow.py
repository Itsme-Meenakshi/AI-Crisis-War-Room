from langgraph.graph import StateGraph, END

from app.graph.state import CrisisState
from app.agents.aggregator import aggregator_agent
from app.agents.executive_summary import executive_summary_agent


def build_graph():

    workflow = StateGraph(CrisisState)

    workflow.add_node("aggregator", aggregator_agent)
    workflow.add_node("summary", executive_summary_agent)

    workflow.set_entry_point("aggregator")

    workflow.add_edge("aggregator", "summary")
    workflow.add_edge("summary", END)

    return workflow.compile()