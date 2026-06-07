# LLM wrapper: OpenRouter-first chat with optional legacy Groq/OpenAI keys.
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
            raise ValueError("GROQ_API_KEY is missing")
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

def _response_error_detail(resp: httpx.Response) -> str:
    try:
        payload = resp.json()
    except ValueError:
        return resp.text[:240].strip() or resp.reason_phrase
    err = payload.get("error")
    if isinstance(err, dict):
        msg = str(err.get("message") or "").strip()
        code = err.get("code")
        if msg and code is not None:
            return f"{msg} (code {code})"
        if msg:
            return msg
    return resp.text[:240].strip() or resp.reason_phrase

async def _post_chat(provider: str, payload: dict) -> httpx.Response:
    for attempt in range(settings.MAX_RETRIES+1):
        r = await http.post(_url(provider), headers=_headers(provider), json=payload)
        if r.status_code in (429,500,502,503,504) and attempt < settings.MAX_RETRIES:
            await asyncio.sleep(0.5*(2**attempt)); continue
        return r
    return r

async def chat_completion(messages: Sequence[Message], model: str, temperature: float=0.2, stream: bool=False):
    provider, model_name = _provider_and_model(model)
    payload = {
        "model": model_name,
        "messages": list(messages),
        "temperature": temperature,
        "max_tokens": 700,
        "stream": stream,
    }
    resp = await _post_chat(provider, payload)
    if resp.status_code >= 400:
        detail = _response_error_detail(resp)
        raise RuntimeError(f"OpenRouter chat failed ({resp.status_code}): {detail}" if provider == "openrouter" else f"{provider} chat failed ({resp.status_code}): {detail}")
    return resp


def _openrouter_model_candidates(primary_model: str | None = None) -> list[str]:
    primary = primary_model or settings.effective_default_model()
    candidates = [primary, settings.OPENROUTER_MODEL]
    return [m for m in dict.fromkeys(candidates) if m.startswith("openrouter/") and not m.endswith(":free")]


def _model_candidates(primary_model: str | None = None, fallback_model: str | None = None) -> list[str]:
    if settings.OPENROUTER_API_KEY:
        return _openrouter_model_candidates(primary_model)

    primary = primary_model or settings.DEFAULT_MODEL
    openai_fallback = fallback_model or settings.OPENAI_MODEL
    candidates: list[str] = [primary]

    if settings.GROQ_API_KEY:
        groq_model = (
            settings.DEFAULT_MODEL
            if settings.DEFAULT_MODEL.startswith("groq/")
            else "groq/llama-3.1-70b-versatile"
        )
        candidates.append(groq_model)

    if settings.OPENAI_API_KEY:
        candidates.append(openai_fallback)

    return list(dict.fromkeys(candidates))


async def smart_chat(messages: Sequence[Message], primary_model: str|None=None, fallback_model: str|None=None, temperature: float=0.2) -> str:
    last_error: Exception | None = None
    text = ""
    for model in _model_candidates(primary_model, fallback_model):
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


async def smart_chat_stream(
    messages: Sequence[Message],
    primary_model: str | None = None,
    fallback_model: str | None = None,
    temperature: float = 0.2,
):
    last_error: Exception | None = None
    for model in _model_candidates(primary_model, fallback_model):
        try:
            return await chat_completion(messages, model, temperature, stream=True)
        except Exception as e:
            last_error = e
            continue
    if last_error:
        raise last_error
    raise RuntimeError("No chat provider available")
