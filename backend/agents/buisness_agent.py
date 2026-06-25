from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.2
)


def business_analysis(crisis: str, context: str):

    prompt = ChatPromptTemplate.from_template("""
You are the Business Risk Agent.

Using the crisis description and retrieved knowledge,
analyze:

• Revenue impact
• Financial losses
• Customer churn risk
• Business continuity

Return ONLY valid JSON.

{{
    "business_risk_level":"",
    "financial_impact":"",
    "customer_churn_risk":"",
    "business_continuity":"",
    "recommendations":[]
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