# LLM wrapper: Groq fast, OpenAI fallback, streaming pass-through.
from typing import Literal, Sequence
import asyncio, httpx
from .config import settings

Role = Literal["system","user","assistant"]
Message = dict  # {role, content}

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

http = httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_S)

def _provider_and_model(name: str):
    if name.startswith("groq/"):
        return "groq", name.split("/",1)[1]
    return "openai", name

def _headers(provider: str):
    if provider == "groq":
        return {"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type":"application/json"}
    return {"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type":"application/json"}

def _url(provider: str):
    return GROQ_URL if provider=="groq" else OPENAI_URL

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
    r = await chat_completion(messages, primary, temperature, stream=False)
    data = r.json()
    text = data["choices"][0]["message"]["content"].strip()
    if len(text) < 120 and settings.OPENAI_API_KEY:
        r2 = await chat_completion(messages, fallback, temperature, stream=False)
        text = r2.json()["choices"][0]["message"]["content"].strip()
    return text
