from typing import TypedDict, List, Optional


class CrisisState(TypedDict):
    # User Input
    crisis_description: str

    # Classification Output
    crisis_type: Optional[str]
    severity: Optional[str]
    stakeholders: List[str]

    # RAG Output
    rag_context: Optional[str]

    # Agent Outputs
    business_analysis: Optional[str]
    legal_analysis: Optional[str]
    operations_analysis: Optional[str]
    pr_analysis: Optional[str]

    # Aggregator Output
    overall_risk: Optional[str]
    recommendations: List[str]

    # Final Output
    executive_summary: Optional[str]