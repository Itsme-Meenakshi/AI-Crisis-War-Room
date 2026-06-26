import uuid
from datetime import datetime
from typing import List, Optional
from app.graph.workflow import build_graph
from app.schemas.response_schema import (
    CrisisAnalyzeResponse, Stakeholder, RiskItem, PerspectiveInsight, CrisisAction, FileAttachment
)

# Compile the LangGraph workflow
workflow_graph = build_graph()

def analyze_crisis_event(title: str, description: str, files: Optional[List] = None) -> CrisisAnalyzeResponse:
    # Build initial state inputs for LangGraph
    # We combine title and description as the crisis description
    full_description = f"{title}\n\n{description}"
    
    initial_state = {
        "crisis_description": full_description,
        "stakeholders": [],
        "recommendations": []
    }
    
    # Run the graph synchronously
    state_result = workflow_graph.invoke(initial_state)
    
    # Map the resulting state to the response schema:
    
    # Map severity string (e.g. "High") to 0-100 integer value
    severity_str = state_result.get("severity", "Medium")
    severity_map = {"Low": 30, "Medium": 55, "High": 82, "Critical": 95}
    severity_val = severity_map.get(severity_str, 55)
    
    # Map stakeholders (convert list of strings to list of Stakeholder objects)
    stakeholders_list = state_result.get("stakeholders", [])
    stakeholders = []
    for s_name in stakeholders_list:
        stakeholders.append(Stakeholder(
            name=s_name,
            impact=75 if severity_str in ["High", "Critical"] else 45,
            sentiment="negative" if severity_str in ["High", "Critical"] else "neutral"
        ))
    if not stakeholders:
        # Provide sensible default stakeholders if not populated
        stakeholders = [
            Stakeholder(name="Customers", impact=80, sentiment="negative"),
            Stakeholder(name="Employees", impact=50, sentiment="neutral"),
            Stakeholder(name="Investors", impact=65, sentiment="negative")
        ]
        
    # Standard risk categories with values
    risks = [
        RiskItem(category="Financial", likelihood=75, impact=70),
        RiskItem(category="Reputation", likelihood=85, impact=80),
        RiskItem(category="Legal", likelihood=60, impact=75),
        RiskItem(category="Operational", likelihood=65, impact=60),
        RiskItem(category="Compliance", likelihood=50, impact=70),
    ]
    
    # Build perspectives matching the tabs in the UI
    perspectives = [
        PerspectiveInsight(
            perspective="Business",
            summary=state_result.get("business_analysis", "Revenue risk is moderate. Prioritize high-value client communication and monitor contract SLA liabilities."),
            recommendations=[
                "Brief the executive leadership team within 1 hour",
                "Assess financial exposure from contract SLAs",
                "Establish customer retention communications"
            ]
        ),
        PerspectiveInsight(
            perspective="PR",
            summary=state_result.get("pr_analysis", "Reputational impact is active. Direct communication with media and stakeholders is required to control the narrative."),
            recommendations=[
                "Publish verified holding statement to media channels",
                "Brief customer-facing staff on talking points",
                "Monitor public sentiment across news and social media"
            ]
        ),
        PerspectiveInsight(
            perspective="Legal",
            summary=state_result.get("legal_analysis", "Compliance and disclosure protocols should be reviewed. Limit external communications to prevent liability expansion."),
            recommendations=[
                "Issue a internal litigation/evidence hold notice",
                "Engage outside legal counsel for regulatory advice",
                "Draft disclosure documentation templates"
            ]
        ),
        PerspectiveInsight(
            perspective="Operations",
            summary=state_result.get("operations_analysis", "Containment must be immediate. Isolate systems and initiate business continuity/recovery checkpoints."),
            recommendations=[
                "Activate technical incident command post",
                "Isolate affected servers and networks",
                "Verify backup integrity and data restore pipelines"
            ]
        )
    ]
    
    # Standard timeline for the crisis
    timeline = [
        CrisisAction(time="0-1h", title="Activate war room & assign roles", owner="Operations", priority="P0"),
        CrisisAction(time="0-2h", title="Issue public holding statement", owner="PR", priority="P0"),
        CrisisAction(time="1-3h", title="Issue litigation hold & restrict communication", owner="Legal", priority="P0"),
        CrisisAction(time="2-6h", title="Assess customer contract and SLA exposure", owner="Business", priority="P1"),
        CrisisAction(time="6-24h", title="Initiate system restoration from backups", owner="Operations", priority="P1"),
    ]
    
    # Convert file attachments
    attachments = []
    if files:
        for f in files:
            attachments.append(FileAttachment(name=f.get("name"), size=f.get("size")))
            
    # Auto-classify category based on text search
    text = (title + " " + description).lower()
    if any(k in text for k in ["breach", "hack", "ransomware", "cyber", "data"]):
        category = "Cybersecurity"
    elif any(k in text for k in ["lawsuit", "regulator", "legal", "court"]):
        category = "Legal & Regulatory"
    elif any(k in text for k in ["pr", "scandal", "executive", "tweet"]):
        category = "Reputation"
    else:
        category = "Operational"
        
    return CrisisAnalyzeResponse(
        id=f"c_{uuid.uuid4().hex[:7]}",
        title=title,
        description=description,
        createdAt=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        status="active",
        severity=severity_val,
        category=category,
        stakeholders=stakeholders,
        risks=risks,
        perspectives=perspectives,
        timeline=timeline,
        attachments=attachments
    )
