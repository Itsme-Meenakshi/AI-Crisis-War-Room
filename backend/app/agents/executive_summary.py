from app.graph.state import CrisisState


def executive_summary_agent(state: CrisisState):

    summary = f"""
    Crisis Type: {state['crisis_type']}

    Severity: {state['severity']}

    Overall Risk: {state['overall_risk']}

    Recommended Actions:
    {', '.join(state['recommendations'])}
    """

    return {
        "executive_summary": summary
    }