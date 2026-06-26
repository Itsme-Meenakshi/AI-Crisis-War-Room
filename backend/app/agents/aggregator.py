import json
import re
from app.graph.state import CrisisState
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

def aggregator_agent(state: CrisisState):
    business = state.get("business_analysis", "No business analysis available.")
    legal = state.get("legal_analysis", "No legal analysis available.")
    operations = state.get("operations_analysis", "No operations analysis available.")
    pr = state.get("pr_analysis", "No PR analysis available.")

    prompt = ChatPromptTemplate.from_template("""
You are the Aggregator Agent in a crisis command center.
Review the four specialist analyses and synthesize them into a unified response.

Return ONLY a valid JSON object with exactly these two keys:
- "overall_risk": strictly one of (Low, Medium, High, Critical)
- "recommendations": a JSON array of exactly 5 short, direct action strings

Example output:
{{"overall_risk": "High", "recommendations": ["Action 1", "Action 2", "Action 3", "Action 4", "Action 5"]}}

Agent Analyses:
- BUSINESS: {business}
- LEGAL: {legal}
- OPERATIONS: {operations}
- PR: {pr}
""")

    chain = prompt | llm

    try:
        response = chain.invoke({
            "business": business,
            "legal": legal,
            "operations": operations,
            "pr": pr
        })
        raw = response.content.strip() if hasattr(response, "content") else str(response).strip()

        # Extract JSON block if wrapped in markdown fences
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(raw)

        return {
            "overall_risk": result.get("overall_risk", "High"),
            "recommendations": result.get("recommendations", [])
        }
    except Exception as e:
        print(f"Error in aggregator_agent: {e}")
        return {
            "overall_risk": "High",
            "recommendations": [
                "Activate incident response command post",
                "Draft internal litigation/evidence hold notice",
                "Publish unified public holding statement",
                "Identify secondary backup region failover status",
                "Begin customer retention and stakeholder communications"
            ]
        }