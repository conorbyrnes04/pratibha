"""Durable Listen archive — Supabase Storage, with a local disk fallback.

Generated speech and tradition cues live here so a later ElevenLabs cancel
does not erase work we already paid to make. The bucket is private; FastAPI
streams bytes. Local `.cache/tts` is only a hot cache.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path

import httpx

from .config import settings

logger = logging.getLogger("pratibha.listen_store")

_CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache" / "tts"
_bucket_ready = False


def _supabase_url() -> str:
    return (settings.SUPABASE_URL or os.getenv("SUPABASE_URL") or "").rstrip("/")


def _service_key() -> str:
    return (
        (settings.SUPABASE_SERVICE_ROLE_KEY or "").strip()
        or (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()
        or (os.getenv("SUPABASE_SERVICE_KEY") or "").strip()
    )


def _bucket() -> str:
    return ((settings.LISTEN_BUCKET or os.getenv("LISTEN_BUCKET") or "listen").strip() or "listen")


def configured() -> bool:
    return bool(_supabase_url() and _service_key())


def local_path(key: str) -> Path:
    return _CACHE_DIR / key.replace("/", "__")


def read_local(key: str) -> bytes | None:
    path = local_path(key)
    if path.is_file():
        data = path.read_bytes()
        if data:
            return data
    return None


def write_local(key: str, data: bytes) -> None:
    path = local_path(key)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    except OSError:
        logger.debug("Listen local cache write failed", exc_info=True)


async def ensure_bucket(client: httpx.AsyncClient) -> bool:
    global _bucket_ready
    if _bucket_ready:
        return True
    if not configured():
        return False
    url = _supabase_url()
    key = _service_key()
    bucket = _bucket()
    headers = {
        "Authorization": f"Bearer {key}",
        "apikey": key,
        "Content-Type": "application/json",
    }
    res = await client.get(f"{url}/storage/v1/bucket/{bucket}", headers=headers, timeout=20.0)
    if res.status_code == 200:
        _bucket_ready = True
        return True
    res = await client.post(
        f"{url}/storage/v1/bucket",
        headers=headers,
        json={
            "id": bucket,
            "name": bucket,
            "public": False,
            "file_size_limit": 52428800,
        },
        timeout=20.0,
    )
    if res.status_code in {200, 201}:
        _bucket_ready = True
        return True
    logger.info("Listen bucket create failed: %s %s", res.status_code, res.text[:200])
    return False


async def get_object(key: str) -> bytes | None:
    cached = read_local(key)
    if cached:
        return cached
    if not configured():
        return None
    async with httpx.AsyncClient() as client:
        if not await ensure_bucket(client):
            return None
        url = _supabase_url()
        svc = _service_key()
        res = await client.get(
            f"{url}/storage/v1/object/{_bucket()}/{key}",
            headers={"Authorization": f"Bearer {svc}", "apikey": svc},
            timeout=40.0,
        )
        if res.status_code >= 400 or not res.content:
            return None
        write_local(key, res.content)
        return res.content


async def put_object(key: str, data: bytes, content_type: str = "audio/mpeg") -> bool:
    if not data:
        return False
    write_local(key, data)
    if not configured():
        return False
    async with httpx.AsyncClient() as client:
        if not await ensure_bucket(client):
            return False
        url = _supabase_url()
        svc = _service_key()
        res = await client.post(
            f"{url}/storage/v1/object/{_bucket()}/{key}",
            headers={
                "Authorization": f"Bearer {svc}",
                "apikey": svc,
                "Content-Type": content_type,
                "x-upsert": "true",
            },
            content=data,
            timeout=60.0,
        )
        if res.status_code >= 400:
            logger.info("Listen object put failed: %s %s", res.status_code, res.text[:200])
            return False
        return True
