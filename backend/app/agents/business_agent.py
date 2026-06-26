from app.graph.state import CrisisState
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

def business_agent(state: CrisisState):
    description = state.get("crisis_description", "")
    context = state.get("rag_context", "No playbooks retrieved.")

    prompt = ChatPromptTemplate.from_template("""
You are the Business Risk Agent in a corporate crisis command center.
Analyze the crisis description using the retrieved incident guidelines.

Write a concise business risk assessment (2-3 sentences max) covering:
- Financial and revenue exposure
- Customer churn and SLA penalties
- Immediate business continuity steps

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
        return {"business_analysis": text}
    except Exception as e:
        print(f"Error in business_agent: {e}")
        return {
            "business_analysis": (
                "The incident poses moderate-to-high financial exposure through potential SLA penalties, "
                "customer churn risk, and reputational damage to key accounts. "
                "Immediate priority is to brief the executive team and activate a customer retention protocol."
            )
        }