from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0.2
)


def classify_crisis(crisis: str):

    prompt = ChatPromptTemplate.from_template("""
You are an expert Crisis Classification Agent.

Analyze the crisis description.

Identify:

1. Crisis Type
2. Severity (Low, Medium, High, Critical)
3. Stakeholders affected

Return ONLY valid JSON.

{{
    "crisis_type":"",
    "severity":"",
    "stakeholders":[]
}}

Crisis Description:
{crisis}
""")

    chain = prompt | llm

    response = chain.invoke({
        "crisis": crisis
    })

    return json.loads(response.content)