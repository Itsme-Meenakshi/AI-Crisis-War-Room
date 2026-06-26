import os
import time
import threading
import requests as http_requests

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from typing import Any, List, Optional

load_dotenv()

api_lock = threading.Lock()

_API_KEY = os.getenv("GOOGLE_API_KEY", "")
_MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
_GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{_MODEL_NAME}:generateContent"


def _call_gemini_rest(prompt: str, api_key: str, model_name: str, retries: int = 5) -> str:
    """
    Call the Gemini REST API directly.
    Sets thinkingBudget=0 so gemini-2.5-flash always returns visible text,
    avoiding the LangChain 'empty content' bug caused by the thinking-mode SDK mismatch.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 1.0,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }

    base_delay = 3.0
    for attempt in range(retries):
        try:
            resp = http_requests.post(url, json=payload, headers=headers, timeout=60)
            if resp.status_code == 429:
                err_body = resp.text.lower()
                is_daily = "perday" in err_body or "per_day" in err_body or "per day" in err_body
                if is_daily:
                    raise RuntimeError(f"Daily quota exhausted: {resp.text}")
                delay = base_delay * (2 ** attempt)
                print(f"[GeminiREST] 429 rate limit, attempt {attempt+1}. Retrying in {delay:.1f}s...")
                time.sleep(delay)
                continue
            resp.raise_for_status()
            data = resp.json()
            # Extract text from first candidate
            candidates = data.get("candidates", [])
            if not candidates:
                raise ValueError(f"No candidates in response: {data}")
            parts = candidates[0].get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts).strip()
            if not text:
                raise ValueError(f"Empty text in response parts: {data}")
            return text
        except (http_requests.exceptions.Timeout, http_requests.exceptions.ConnectionError) as e:
            delay = base_delay * (2 ** attempt)
            print(f"[GeminiREST] Network error attempt {attempt+1}: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)

    raise RuntimeError(f"Gemini REST API failed after {retries} attempts")


class GeminiRestLLM(BaseChatModel):
    """
    LangChain-compatible chat model that calls Gemini via REST with
    thinkingBudget=0 to avoid the empty-content SDK bug.
    All calls are serialized through a threading.Lock to respect RPM limits.
    """
    model_name: str = _MODEL_NAME
    api_key: str = _API_KEY

    @property
    def _llm_type(self) -> str:
        return "gemini-rest"

    def _messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        parts = []
        for m in messages:
            if isinstance(m, SystemMessage):
                parts.append(f"[SYSTEM INSTRUCTION]\n{m.content}")
            elif isinstance(m, HumanMessage):
                parts.append(m.content)
            elif isinstance(m, AIMessage):
                parts.append(f"[ASSISTANT]\n{m.content}")
            else:
                parts.append(str(m.content))
        return "\n\n".join(parts)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        prompt = self._messages_to_prompt(messages)
        with api_lock:
            time.sleep(1.0)  # polite gap between API calls
            text = _call_gemini_rest(prompt, self.api_key, self.model_name)
        msg = AIMessage(content=text)
        return ChatResult(generations=[ChatGeneration(message=msg)])


# Singleton instance imported by all agents
llm = GeminiRestLLM(model_name=_MODEL_NAME, api_key=_API_KEY)