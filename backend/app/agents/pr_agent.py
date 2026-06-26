from app.graph.state import CrisisState
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

def pr_agent(state: CrisisState):
    description = state.get("crisis_description", "")
    context = state.get("rag_context", "No playbooks retrieved.")

    prompt = ChatPromptTemplate.from_template("""
You are the Public Relations & Reputation Agent in a corporate crisis command center.
Analyze the crisis description using the retrieved incident guidelines.

Write a concise reputational risk assessment (2-3 sentences max) covering:
- Public messaging and customer communication strategy
- Guidelines for holding statements and spokesperson briefings
- Sentiment monitoring approach across media and social channels

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
        return {"pr_analysis": text}
    except Exception as e:
        print(f"Error in pr_agent: {e}")
        return {
            "pr_analysis": (
                "Public sentiment is trending negative and a factual, empathetic holding statement must be issued "
                "within two hours to control the narrative. Spokespersons should be briefed on approved talking points "
                "and sentiment should be monitored hourly across news, social media, and customer support channels."
            )
        }