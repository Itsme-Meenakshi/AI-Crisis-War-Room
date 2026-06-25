from typing import TypedDict, List, Optional


class CrisisState(TypedDict):
    # Input
    crisis_description: str

    # Classification
    crisis_type: Optional[str]
    severity: Optional[str]
    stakeholders: List[str]

    # RAG
    rag_context: Optional[str]

    # Agent Outputs
    business_analysis: Optional[str]
    legal_analysis: Optional[str]
    operations_analysis: Optional[str]
    pr_analysis: Optional[str]

    # Final Decision
    overall_risk: Optional[str]
    recommendations: List[str]

    # Final Report
    executive_summary: Optional[str]