from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.2
)


def operations_analysis(crisis: str, context: str):

    prompt = ChatPromptTemplate.from_template("""
You are the Operations Agent.

Analyze:

• Technical impact
• Operational disruption
• Recovery actions
• Service continuity

Return ONLY valid JSON.

{{
    "operational_risk_level":"",
    "technical_impact":"",
    "service_continuity":"",
    "recovery_actions":[]
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