from langgraph.graph import StateGraph, START, END # type: ignore

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

    graph = StateGraph(CrisisState)

    graph.add_node("classifier", classifier_agent)
    graph.add_node("rag", rag_agent)

    graph.add_node("business", business_agent)
    graph.add_node("legal", legal_agent)
    graph.add_node("operations", operations_agent)
    graph.add_node("pr", pr_agent)

    graph.add_node("aggregator", aggregator_agent)
    graph.add_node("summary", executive_summary_agent)

    graph.add_edge(START, "classifier")

    graph.add_edge("classifier", "rag")

    # Fan-out
    graph.add_edge("rag", "business")
    graph.add_edge("rag", "legal")
    graph.add_edge("rag", "operations")
    graph.add_edge("rag", "pr")

    # Fan-in
    graph.add_edge("business", "aggregator")
    graph.add_edge("legal", "aggregator")
    graph.add_edge("operations", "aggregator")
    graph.add_edge("pr", "aggregator")

    graph.add_edge("aggregator", "summary")

    graph.add_edge("summary", END)

    return graph.compile()