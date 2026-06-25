from langgraph.graph import StateGraph, END # type: ignore

from app.graph.state import CrisisState

from app.agents.classifier import classifier_agent
from app.agents.rag_node import rag_agent
from app.agents.business_agent import business_agent
from app.agents.legal_agent import legal_agent
from app.agents.operations_agent import operations_agent
from app.agents.pr_agent import pr_agent
from app.agents.aggregator import aggregator_agent
from app.agents.executive_summary import executive_summary_agent


def build_graph():

    workflow = StateGraph(CrisisState)

    # Nodes
    workflow.add_node("classifier", classifier_agent)
    workflow.add_node("rag", rag_agent)

    workflow.add_node("business", business_agent)
    workflow.add_node("legal", legal_agent)
    workflow.add_node("operations", operations_agent)
    workflow.add_node("pr", pr_agent)

    workflow.add_node("aggregator", aggregator_agent)
    workflow.add_node("summary", executive_summary_agent)

    # Entry Point
    workflow.set_entry_point("classifier")

    # Flow
    workflow.add_edge("classifier", "rag")

    workflow.add_edge("rag", "business")
    workflow.add_edge("business", "legal")
    workflow.add_edge("legal", "operations")
    workflow.add_edge("operations", "pr")
    workflow.add_edge("pr", "aggregator")

    workflow.add_edge("aggregator", "summary")

    workflow.add_edge("summary", END)

    return workflow.compile()