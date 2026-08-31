"""Convex JWT verification for protected API routes.

Convex signs user tokens with RS256. The public key can be retrieved from
the Convex deployment's JWKS endpoint.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

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


def _convex_url() -> str | None:
    """Get the Convex deployment URL from environment."""
    url = (
        os.getenv("NEXT_PUBLIC_CONVEX_URL")
        or getattr(settings, "NEXT_PUBLIC_CONVEX_URL", None)
        or ""
    ).strip().rstrip("/")
    return url or None


def _get_jwks_client() -> PyJWKClient | None:
    """Get or create the JWKS client for Convex token verification."""
    global _jwks_client, _jwks_client_url
    base = _convex_url()
    if not base:
        return None
    
    # Convex JWKS endpoint
    jwks_url = f"{base}/.well-known/jwks.json"
    
    if _jwks_client is None or _jwks_client_url != jwks_url:
        _jwks_client = PyJWKClient(jwks_url, cache_keys=True, lifespan=3600)
        _jwks_client_url = jwks_url
    return _jwks_client


def auth_configured() -> bool:
    """Check if Convex auth is configured."""
    return bool(_convex_url())


def verify_bearer_token(token: str) -> AuthUser:
    """Verify a Convex JWT token and return the user."""
    jwks = _get_jwks_client()
    if jwks is None:
        raise HTTPException(
            status_code=503,
            detail="Auth is not configured (NEXT_PUBLIC_CONVEX_URL)."
        )

    try:
        # Get the signing key from JWKS
        key = jwks.get_signing_key_from_jwt(token).key
        
        # Decode and verify the token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            options={"require": ["sub", "exp", "iss"]},
        )
    except Exception as exc:
        logger.info("JWT rejected: %s", exc)
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
