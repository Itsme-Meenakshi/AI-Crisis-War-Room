from app.graph.state import CrisisState


def aggregator_agent(state: CrisisState):

    combined_analysis = f"""
    BUSINESS:
    {state['business_analysis']}

    LEGAL:
    {state['legal_analysis']}

    OPERATIONS:
    {state['operations_analysis']}

    PR:
    {state['pr_analysis']}
    """

    return {
        "overall_risk": "High",
        "recommendations": [
            "Activate incident response team",
            "Notify stakeholders",
            "Begin recovery process"
        ]
    }