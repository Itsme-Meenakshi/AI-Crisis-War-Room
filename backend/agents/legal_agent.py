from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.2
)


def legal_analysis(crisis: str, context: str):

    prompt = ChatPromptTemplate.from_template("""
You are the Legal Compliance Agent.

Analyze:

• Legal exposure
• Compliance violations
• Regulatory reporting requirements

Return ONLY valid JSON.

{{
    "legal_risk_level":"",
    "legal_exposure":"",
    "compliance_recommendations":[],
    "regulatory_reporting":""
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