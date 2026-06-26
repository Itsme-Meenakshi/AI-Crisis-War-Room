import json
import re
from app.graph.state import CrisisState
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

def classifier_agent(state: CrisisState):
    description = state.get("crisis_description", "")

    prompt = ChatPromptTemplate.from_template("""
You are an expert Crisis Classification Agent.
Analyze the crisis description below and return ONLY a valid JSON object.

The JSON must contain exactly these three keys:
- "crisis_type": one of (Cybersecurity, Outage, Reputation, Legal & Regulatory, Operational)
- "severity": strictly one of (Low, Medium, High, Critical)
- "stakeholders": a JSON array of strings, e.g. ["Customers", "Employees"]

Example output:
{{"crisis_type": "Cybersecurity", "severity": "High", "stakeholders": ["Customers", "Regulators"]}}

Crisis Description:
{description}
""")

    chain = prompt | llm

    try:
        response = chain.invoke({"description": description})
        raw = response.content.strip() if hasattr(response, "content") else str(response).strip()

        # Extract JSON block if wrapped in markdown fences
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(raw)

        return {
            "crisis_type": result.get("crisis_type", "Operational"),
            "severity": result.get("severity", "Medium"),
            "stakeholders": result.get("stakeholders", ["Customers", "Employees"])
        }
    except Exception as e:
        print(f"Error in classifier_agent: {e}")
        # Keyword-based fallback classification
        text = description.lower()
        if any(k in text for k in ["breach", "hack", "cyber", "ransomware", "data leak"]):
            crisis_type, severity = "Cybersecurity", "High"
        elif any(k in text for k in ["lawsuit", "regulator", "court", "legal"]):
            crisis_type, severity = "Legal & Regulatory", "High"
        elif any(k in text for k in ["viral", "media", "pr", "scandal", "executive"]):
            crisis_type, severity = "Reputation", "Medium"
        elif any(k in text for k in ["outage", "down", "failure", "crash"]):
            crisis_type, severity = "Outage", "High"
        else:
            crisis_type, severity = "Operational", "Medium"

        return {
            "crisis_type": crisis_type,
            "severity": severity,
            "stakeholders": ["Customers", "Employees", "Investors"]
        }