from app.models.llm import llm

response = llm.invoke(
    "Explain ransomware in one sentence."
)

print(response.content)