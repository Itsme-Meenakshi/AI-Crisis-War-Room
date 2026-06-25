from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.2
)


def pr_analysis(crisis: str, context: str):

    prompt = ChatPromptTemplate.from_template("""
You are the Public Relations Agent.

Analyze:

• Reputation damage
• Media response
• Public communication
• Stakeholder communication

Return ONLY valid JSON.

{{
    "reputation_risk_level":"",
    "media_response":"",
    "communication_strategy":"",
    "public_recommendations":[]
}}

Context:
{context}

Crisis:
{crisis}
""")

    chain = prompt | llm

    response = chain.invoke({
        "crisis": crisis,
        "context": context
    })

    return json.loads(response.content)