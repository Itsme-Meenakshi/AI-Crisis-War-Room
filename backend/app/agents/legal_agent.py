from app.graph.state import CrisisState
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

def legal_agent(state: CrisisState):
    description = state.get("crisis_description", "")
    context = state.get("rag_context", "No playbooks retrieved.")

    prompt = ChatPromptTemplate.from_template("""
You are the Legal & Compliance Risk Agent in a corporate crisis command center.
Analyze the crisis description using the retrieved incident guidelines.

Write a concise legal risk assessment (2-3 sentences max) covering:
- Regulatory disclosure obligations (e.g. GDPR, HIPAA, SEC)
- Contractual liabilities and lawsuit exposure
- Immediate steps for evidence hold and restricting communications

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
        return {"legal_analysis": text}
    except Exception as e:
        print(f"Error in legal_agent: {e}")
        return {
            "legal_analysis": (
                "Potential regulatory disclosure obligations under applicable data-protection laws should be assessed immediately. "
                "Legal counsel should issue an internal evidence hold, restrict public commentary, and prepare draft notifications "
                "for relevant regulatory bodies."
            )
        }