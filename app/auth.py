"""Convex JWT verification for protected API routes.

Convex signs user tokens with RS256. The public key can be retrieved from
the Convex deployment's JWKS endpoint.
"""
from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
from dataclasses import dataclass
from typing import Any

import jwt
from fastapi import Depends, HTTPException, Request
from jwt import PyJWKSet

from .config import settings

logger = logging.getLogger("pratibha.auth")

_jwks_keys: list[Any] | None = None
_jwks_url_cached: str | None = None
_jwks_fetched_at: float = 0.0
_JWKS_TTL_S = 3600.0


@dataclass(frozen=True)
class AuthUser:
    id: str
    email: str | None = None
    claims: dict[str, Any] | None = None


def _convex_url() -> str | None:
    """Get the Convex deployment URL from environment."""
    url = (
        os.getenv("NEXT_PUBLIC_CONVEX_URL")
        or getattr(settings, "NEXT_PUBLIC_CONVEX_URL", None)
        or ""
    ).strip().rstrip("/")
    return url or None


def _convex_site_url() -> str | None:
    """HTTP site origin Convex Auth uses as `iss` and JWKS host."""
    explicit = (
        os.getenv("NEXT_PUBLIC_CONVEX_SITE_URL")
        or getattr(settings, "NEXT_PUBLIC_CONVEX_SITE_URL", None)
        or ""
    ).strip().rstrip("/")
    if explicit:
        return explicit
    cloud = _convex_url()
    if cloud and cloud.endswith(".convex.cloud"):
        return cloud[: -len(".convex.cloud")] + ".convex.site"
    return None


def _jwks_url() -> str | None:
    """Convex Auth publishes JWKS on `.convex.site`, not `.convex.cloud`."""
    site = _convex_site_url()
    if site:
        return f"{site}/.well-known/jwks.json"
    base = _convex_url()
    if not base:
        return None
    return f"{base}/.well-known/jwks.json"


def _load_jwks_keys() -> list[Any]:
    """Load Convex Auth signing keys.

    Convex publishes RSA keys on `.convex.site` without a `kid`. PyJWKClient
    drops those, so we read the set ourselves.
    """
    global _jwks_keys, _jwks_url_cached, _jwks_fetched_at
    jwks_url = _jwks_url()
    if not jwks_url:
        return []
    now = time.time()
    if (
        _jwks_keys
        and _jwks_url_cached == jwks_url
        and now - _jwks_fetched_at < _JWKS_TTL_S
    ):
        return _jwks_keys
    with urllib.request.urlopen(jwks_url, timeout=8) as response:
        data = json.load(response)
    keys = [
        key
        for key in PyJWKSet.from_dict(data).keys
        if key.public_key_use in ("sig", None)
    ]
    _jwks_keys = keys
    _jwks_url_cached = jwks_url
    _jwks_fetched_at = now
    return keys


def _signing_key(token: str):
    keys = _load_jwks_keys()
    if not keys:
        raise RuntimeError("Convex JWKS has no signing keys")
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    if kid:
        for key in keys:
            if key.key_id == kid:
                return key.key
    return keys[0].key


def auth_configured() -> bool:
    """Check if Convex auth is configured."""
    return bool(_convex_url())


def verify_bearer_token(token: str) -> AuthUser:
    """Verify a Convex JWT token and return the user."""
    if not _jwks_url():
        raise HTTPException(
            status_code=503,
            detail="Auth is not configured (NEXT_PUBLIC_CONVEX_URL)."
        )

    try:
        payload = jwt.decode(
            token,
            _signing_key(token),
            algorithms=["RS256"],
            audience="convex",
            options={"require": ["sub", "exp", "iss"]},
        )
    except Exception as exc:
        logger.warning("JWT rejected: %s", exc)
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    sub = str(payload.get("sub") or "").strip()
    if not sub:
        raise HTTPException(status_code=401, detail="Token missing subject")
    
    # Extract email from token if present
    email = payload.get("email")
    
    return AuthUser(
        id=sub,
        email=str(email) if email else None,
        claims=payload
    )


def _extract_bearer(request: Request) -> str | None:
    """Extract bearer token from Authorization header."""
    header = request.headers.get("authorization") or request.headers.get("Authorization") or ""
    if not header.lower().startswith("bearer "):
        return None
    token = header[7:].strip()
    return token or None


async def optional_user(request: Request) -> AuthUser | None:
    """Optionally get the authenticated user from the request."""
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
    """Require an authenticated user for this request."""
    token = _extract_bearer(request)
    if not token:
        raise HTTPException(status_code=401, detail="Sign in required")
    return verify_bearer_token(token)


async def require_user_if_configured(request: Request) -> AuthUser | None:
    """Require a Convex JWT when auth is configured (production). Allow local/dev without it."""
    if not auth_configured():
        return None
    return await require_user(request)
