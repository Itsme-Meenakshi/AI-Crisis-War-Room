from app.graph.state import CrisisState
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

def operations_agent(state: CrisisState):
    description = state.get("crisis_description", "")
    context = state.get("rag_context", "No playbooks retrieved.")

    prompt = ChatPromptTemplate.from_template("""
You are the Operations & Technical Containment Agent in a corporate crisis command center.
Analyze the crisis description using the retrieved incident guidelines.

Write a concise operational risk assessment (2-3 sentences max) covering:
- Technical system containment and quarantine actions
- Root-cause identification checkpoints
- Restoration milestones and backup integrity checks

Do NOT use bullet points, headers, or JSON. Write plain prose only.

Retrieved Context:
{context}

Crisis Description:
{description}
""")
    chain = prompt | llm

    try:
        response = chain.invoke({"description": description, "context": context})
        text = response.content.strip() if hasattr(response, "content") and response.content else ""
        if not text:
            raise ValueError("Empty response from model")
        return {"operations_analysis": text}
    except Exception as e:
        print(f"Error in operations_agent: {e}")
        return {
            "operations_analysis": (
                "Immediate technical containment is the top priority — isolate affected systems and block lateral movement. "
                "An incident command post should be established with 30-minute status checkpoints to track root-cause identification "
                "and validate backup integrity before initiating any restoration procedures."
            )
        }