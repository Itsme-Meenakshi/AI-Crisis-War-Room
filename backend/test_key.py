import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")

print("Env Model Name:", model_name)
print("API Key:", api_key[:15] + "..." if api_key else "None")

try:
    chat = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
    res = chat.invoke("Hello")
    print("Response:", res.content)
except Exception as e:
    print("Error:", e)
