import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL_NAME", "gemini-2.5-flash")

print(f"Testing model: {model}")
print("=" * 50)

# -----------------------------------------------------------------
# Approach 1: thinking_budget=0 via direct param
# -----------------------------------------------------------------
print("\n[Approach 1] thinking_budget=0 as direct param...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm1 = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=1,
        thinking_budget=0,
    )
    r1 = llm1.invoke("Say the word: hello")
    print(f"  OK -> content: '{r1.content[:80]}'")
except Exception as e:
    print(f"  FAIL -> {e}")

# -----------------------------------------------------------------
# Approach 2: model_kwargs with thinkingConfig
# -----------------------------------------------------------------
print("\n[Approach 2] model_kwargs thinkingConfig...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm2 = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=1,
        model_kwargs={
            "generation_config": {
                "thinking_config": {"thinking_budget": 0}
            }
        }
    )
    r2 = llm2.invoke("Say the word: hello")
    print(f"  OK -> content: '{r2.content[:80]}'")
except Exception as e:
    print(f"  FAIL -> {e}")

# -----------------------------------------------------------------
# Approach 3: Use google-generativeai directly (bypass LangChain)
# -----------------------------------------------------------------
print("\n[Approach 3] google.generativeai SDK directly...")
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    g_model = genai.GenerativeModel(model)
    response = g_model.generate_content(
        "Say the word: hello",
        generation_config=genai.GenerationConfig(
            temperature=1,
            thinking_config=genai.protos.ThinkingConfig(thinking_budget=0)
        )
    )
    print(f"  OK -> text: '{response.text[:80]}'")
except Exception as e:
    print(f"  FAIL -> {e}")

# -----------------------------------------------------------------
# Approach 4: flash-lite model (no thinking mode)
# -----------------------------------------------------------------
print("\n[Approach 4] gemini-2.5-flash-lite (no thinking mode)...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm4 = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0.3,
    )
    r4 = llm4.invoke("Say the word: hello")
    print(f"  OK -> content: '{r4.content[:80]}'")
except Exception as e:
    print(f"  FAIL -> {e}")

# -----------------------------------------------------------------
# Approach 5: gemini-2.0-flash (no thinking mode)
# -----------------------------------------------------------------
print("\n[Approach 5] gemini-2.0-flash (no thinking by default)...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm5 = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3,
    )
    r5 = llm5.invoke("Say the word: hello")
    print(f"  OK -> content: '{r5.content[:80]}'")
except Exception as e:
    print(f"  FAIL -> {e}")

print("\n" + "=" * 50)
print("Done.")
