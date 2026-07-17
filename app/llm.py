# LLM wrapper: OpenRouter-only chat. (Groq/OpenAI are no longer chat providers;
# OpenAI remains only for RAG embeddings elsewhere.)
from typing import Literal, Sequence
import asyncio, httpx
from .config import settings

Role = Literal["system","user","assistant"]
Message = dict  # {role, content}

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

http = httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_S)

def _provider_and_model(name: str):
    # Everything routes through OpenRouter. Strip a leading "openrouter/" if present;
    # tolerate legacy "groq/"/bare ids by treating the remainder as the OpenRouter id.
    model = name.split("/", 1)[1] if name.startswith(("openrouter/", "groq/")) else name
    return "openrouter", model

def _headers(provider: str):
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing")
    headers = {"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    if settings.OPENROUTER_SITE_URL:
        headers["HTTP-Referer"] = settings.OPENROUTER_SITE_URL
    if settings.OPENROUTER_APP_NAME:
        headers["X-Title"] = settings.OPENROUTER_APP_NAME
    return headers

def _url(provider: str):
    return OPENROUTER_URL

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

async def chat_completion(messages: Sequence[Message], model: str, temperature: float=0.2, stream: bool=False, max_tokens: int | None = None):
    provider, model_name = _provider_and_model(model)
    payload = {
        "model": model_name,
        "messages": list(messages),
        "temperature": temperature,
        "max_tokens": max_tokens or settings.CHAT_MAX_TOKENS,
        "stream": stream,
    }
    resp = await _post_chat(provider, payload)
    if resp.status_code >= 400:
        detail = _response_error_detail(resp)
        raise RuntimeError(f"OpenRouter chat failed ({resp.status_code}): {detail}" if provider == "openrouter" else f"{provider} chat failed ({resp.status_code}): {detail}")
    return resp


def _model_candidates(primary_model: str | None = None, fallback_model: str | None = None) -> list[str]:
    """Ordered OpenRouter model ids to try. Always non-empty when a request or
    default model is set, so chat never silently returns an empty answer."""
    primary = (primary_model or "").strip() or settings.effective_default_model()
    candidates = [primary, settings.effective_default_model(), settings.OPENROUTER_MODEL]
    # Ensure every id is OpenRouter-routed; bare ids get an "openrouter/" prefix.
    normalized: list[str] = []
    for m in candidates:
        m = (m or "").strip()
        if not m:
            continue
        normalized.append(m if m.startswith("openrouter/") else f"openrouter/{m}")
    deduped = list(dict.fromkeys(normalized))
    return deduped or [settings.OPENROUTER_MODEL]


async def smart_chat(messages: Sequence[Message], primary_model: str|None=None, fallback_model: str|None=None, temperature: float=0.2, max_tokens: int | None = None) -> str:
    last_error: Exception | None = None
    text = ""
    for model in _model_candidates(primary_model, fallback_model):
        try:
            r = await chat_completion(messages, model, temperature, stream=False, max_tokens=max_tokens)
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
