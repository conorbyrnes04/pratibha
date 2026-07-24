"""Supabase JWT verification for protected API routes.

New Supabase projects sign user tokens with ES256 and publish keys at
``{SUPABASE_URL}/auth/v1/.well-known/jwks.json``. Legacy projects may still
use an HS256 shared ``SUPABASE_JWT_SECRET``.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

import httpx
import jwt
from fastapi import Depends, HTTPException, Request
from jwt import PyJWKClient

from .config import settings

logger = logging.getLogger("pratibha.auth")

_jwks_client: PyJWKClient | None = None
_jwks_client_url: str | None = None


@dataclass(frozen=True)
class AuthUser:
    id: str
    email: str | None = None
    claims: dict[str, Any] | None = None


def _supabase_url() -> str | None:
    url = (settings.SUPABASE_URL or "").strip().rstrip("/")
    return url or None


def _jwt_secret() -> str | None:
    secret = (settings.SUPABASE_JWT_SECRET or "").strip()
    if not secret:
        return None
    # Guard: anon/service_role API keys are JWTs themselves, not signing secrets.
    if secret.startswith("eyJ") and secret.count(".") == 2:
        logger.warning(
            "SUPABASE_JWT_SECRET looks like an API key (anon/service_role), not a signing secret; "
            "ignoring it and using JWKS if available."
        )
        return None
    return secret


def _get_jwks_client() -> PyJWKClient | None:
    global _jwks_client, _jwks_client_url
    base = _supabase_url()
    if not base:
        return None
    jwks_url = f"{base}/auth/v1/.well-known/jwks.json"
    if _jwks_client is None or _jwks_client_url != jwks_url:
        _jwks_client = PyJWKClient(jwks_url, cache_keys=True, lifespan=3600)
        _jwks_client_url = jwks_url
    return _jwks_client


def auth_configured() -> bool:
    return bool(_supabase_url() or _jwt_secret())


def verify_bearer_token(token: str) -> AuthUser:
    payload: dict[str, Any] | None = None
    errors: list[str] = []

    # Prefer JWKS (ES256) — current Supabase default.
    jwks = _get_jwks_client()
    if jwks is not None:
        try:
            key = jwks.get_signing_key_from_jwt(token).key
            payload = jwt.decode(
                token,
                key,
                algorithms=["ES256", "RS256"],
                audience="authenticated",
                options={"require": ["sub", "exp"]},
            )
        except Exception as exc:  # noqa: BLE001 — fall through to legacy secret
            errors.append(f"jwks:{exc}")

    # Legacy HS256 shared secret.
    if payload is None:
        secret = _jwt_secret()
        if secret:
            try:
                payload = jwt.decode(
                    token,
                    secret,
                    algorithms=["HS256"],
                    audience="authenticated",
                    options={"require": ["sub", "exp"]},
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(f"hs256:{exc}")

    if payload is None:
        if not auth_configured():
            raise HTTPException(status_code=503, detail="Auth is not configured (SUPABASE_URL / SUPABASE_JWT_SECRET).")
        logger.info("JWT rejected: %s", "; ".join(errors) or "no verifier")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    sub = str(payload.get("sub") or "").strip()
    if not sub:
        raise HTTPException(status_code=401, detail="Token missing subject")
    email = payload.get("email")
    return AuthUser(id=sub, email=str(email) if email else None, claims=payload)


def _extract_bearer(request: Request) -> str | None:
    header = request.headers.get("authorization") or request.headers.get("Authorization") or ""
    if not header.lower().startswith("bearer "):
        return None
    token = header[7:].strip()
    return token or None


async def optional_user(request: Request) -> AuthUser | None:
    token = _extract_bearer(request)
    if not token:
        return None
    if not auth_configured():
        return None
    try:
        return verify_bearer_token(token)
    except HTTPException:
        return None


async def require_user(request: Request) -> AuthUser:
    token = _extract_bearer(request)
    if not token:
        raise HTTPException(status_code=401, detail="Sign in required")
    return verify_bearer_token(token)


# Warm JWKS once at import when URL is present (best-effort).
def _warm_jwks() -> None:
    client = _get_jwks_client()
    if client is None:
        return
    try:
        # Force a fetch so the first request isn't cold.
        with httpx.Client(timeout=10.0) as http:
            http.get(f"{_supabase_url()}/auth/v1/.well-known/jwks.json")
        _ = time.time()
    except Exception:
        logger.debug("JWKS warm failed", exc_info=True)


_warm_jwks()
