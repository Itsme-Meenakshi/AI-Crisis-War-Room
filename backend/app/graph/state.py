from typing import Annotated, Optional
from typing_extensions import TypedDict

from operator import add


class CrisisState(TypedDict):
    # ======================
    # User Input
    # ======================
    crisis_description: str

    # ======================
    # Classification
    # ======================
    crisis_type: Optional[str]
    severity: Optional[str]
    stakeholders: Annotated[list[str], add]

    # ======================
    # RAG
    # ======================
    rag_context: Optional[str]

    # ======================
    # Agent Outputs
    # ======================
    business_analysis: Optional[str]
    legal_analysis: Optional[str]
    operations_analysis: Optional[str]
    pr_analysis: Optional[str]

    # ======================
    # Aggregated Results
    # ======================
    overall_risk: Optional[str]
    recommendations: Annotated[list[str], add]

    # ======================
    # Final Output
    # ======================
    executive_summary: Optional[str]