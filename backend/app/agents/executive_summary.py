from app.graph.state import CrisisState
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

def executive_summary_agent(state: CrisisState):
    description = state.get("crisis_description", "")
    crisis_type = state.get("crisis_type", "Operational")
    severity = state.get("severity", "Medium")
    overall_risk = state.get("overall_risk", "High")
    recommendations = state.get("recommendations", [])
    
    prompt = ChatPromptTemplate.from_template("""
You are the Executive Summary Agent at a crisis command center.
Your task is to write a highly professional, concise management-level executive summary brief for corporate leadership.

The brief must:
- Summarize the crisis event and its primary driver in 1 sentence.
- Highlight the key risk categories, risk levels (Severity: {severity}, Overall Risk: {overall_risk}), and core potential business exposures in 1-2 sentences.
- Outline the critical path response strategy based on the recommendations.

Keep the summary to exactly 1-2 paragraphs. Keep it professional, objective, and clear. Do not use bullet points or formatting labels (such as "Summary:", "Risk:", etc.).

Crisis Description:
{description}

Crisis Type: {crisis_type}
Severity: {severity}
Overall Risk: {overall_risk}

Prioritized Recommendations:
{recommendations_str}
""")
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "description": description,
            "crisis_type": crisis_type,
            "severity": severity,
            "overall_risk": overall_risk,
            "recommendations_str": "\n".join([f"- {r}" for r in recommendations])
        })
        text = response.content.strip() if hasattr(response, "content") and response.content else ""
        if not text:
            raise ValueError("Empty response from model")
        return {
            "executive_summary": text
        }
    except Exception as e:
        print(f"Error in executive_summary_agent: {e}")
        fallback_summary = f"""
The organization is responding to an active {crisis_type} event with a severity score of {severity} and an overall risk level of {overall_risk}. 
Primary operational priority is to establish containment and safeguard critical infrastructure. 
Key actions underway include: {', '.join(recommendations[:3])}.
"""
        return {
            "executive_summary": fallback_summary.strip()
        }