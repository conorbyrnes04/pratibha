# LLM wrapper: Groq fast, OpenAI fallback, streaming pass-through.
from typing import Literal, Sequence
import asyncio, httpx
from .config import settings

Role = Literal["system","user","assistant"]
Message = dict  # {role, content}

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

http = httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_S)

def _provider_and_model(name: str):
    if name.startswith("groq/"):
        if not settings.GROQ_API_KEY:
            if settings.OPENROUTER_API_KEY:
                fallback = settings.OPENROUTER_MODEL
                return "openrouter", fallback.split("/", 1)[1] if fallback.startswith("openrouter/") else fallback
            return "openai", settings.OPENAI_MODEL
        return "groq", name.split("/",1)[1]
    if name.startswith("openrouter/"):
        return "openrouter", name.split("/", 1)[1]
    return "openai", name

def _headers(provider: str):
    if provider == "groq":
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing")
        return {"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type":"application/json"}
    if provider == "openrouter":
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing")
        headers = {"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}", "Content-Type":"application/json"}
        if settings.OPENROUTER_SITE_URL:
            headers["HTTP-Referer"] = settings.OPENROUTER_SITE_URL
        if settings.OPENROUTER_APP_NAME:
            headers["X-Title"] = settings.OPENROUTER_APP_NAME
        return headers
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing")
    return {"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type":"application/json"}

def _url(provider: str):
    if provider == "groq":
        return GROQ_URL
    if provider == "openrouter":
        return OPENROUTER_URL
    return OPENAI_URL

async def _post_chat(provider: str, payload: dict) -> httpx.Response:
    for attempt in range(settings.MAX_RETRIES+1):
        r = await http.post(_url(provider), headers=_headers(provider), json=payload)
        if r.status_code in (429,500,502,503,504) and attempt < settings.MAX_RETRIES:
            await asyncio.sleep(0.5*(2**attempt)); continue
        return r
    return r

async def chat_completion(messages: Sequence[Message], model: str, temperature: float=0.2, stream: bool=False):
    provider, model_name = _provider_and_model(model)
    payload = {"model": model_name, "messages": list(messages), "temperature": temperature, "stream": stream}
    resp = await _post_chat(provider, payload)
    resp.raise_for_status()
    return resp

async def smart_chat(messages: Sequence[Message], primary_model: str|None=None, fallback_model: str|None=None, temperature: float=0.2) -> str:
    primary = primary_model or settings.DEFAULT_MODEL
    fallback = fallback_model or settings.OPENAI_MODEL
    candidates = [primary]
    if settings.OPENROUTER_API_KEY:
        candidates.append(settings.OPENROUTER_MODEL)
        # Keep resilient OpenRouter free-model fallbacks when one is rate-limited.
        candidates.append("openrouter/meta-llama/llama-3.3-70b-instruct:free")
        candidates.append("openrouter/google/gemma-3-12b-it:free")
        candidates.append("openrouter/openai/gpt-oss-20b:free")
    if settings.OPENAI_API_KEY:
        candidates.append(fallback)

    # Deduplicate while preserving order.
    candidates = list(dict.fromkeys(candidates))

    last_error: Exception | None = None
    text = ""
    for model in candidates:
        try:
            r = await chat_completion(messages, model, temperature, stream=False)
            data = r.json()
            text = data["choices"][0]["message"]["content"].strip()
            if text:
                return text
        except Exception as e:
            last_error = e
            continue

    if last_error:
        raise last_error
    return text
