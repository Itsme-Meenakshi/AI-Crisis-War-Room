from app.graph.state import CrisisState

def classifier_agent(state: CrisisState):
    return {
        "crisis_type": "Cyber Attack",
        "severity": "High",
        "stakeholders": ["Customers", "Employees"]
    }