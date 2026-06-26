import sys
sys.path.insert(0, ".")
from app.models.llm import llm
from langchain_core.prompts import ChatPromptTemplate

print("Testing GeminiDirectLLM with a simple prompt...")

prompt = ChatPromptTemplate.from_template("In one sentence, describe what a data breach is: {topic}")
chain = prompt | llm

try:
    result = chain.invoke({"topic": "cybersecurity incident"})
    print(f"SUCCESS! Response: {result.content[:200]}")
except Exception as e:
    print(f"FAILED: {e}")
