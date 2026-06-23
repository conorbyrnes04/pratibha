"""Pydantic settings. Edit values in `.env`.
"""
import ssl as _ssl
from urllib.parse import parse_qs, unquote, urlparse

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str = "openrouter/meta-llama/llama-3.3-70b-instruct"
    OPENROUTER_SITE_URL: str | None = None
    OPENROUTER_APP_NAME: str = "Pratibha"
    DEFAULT_MODEL: str = "groq/llama-3.1-70b-versatile"
    OPENAI_MODEL: str = "gpt-4o-mini"
    USE_RAG: bool = False
    VECTOR_BACKEND: str = "pgvector"
    REQUEST_TIMEOUT_S: float = 20.0
    MAX_RETRIES: int = 2
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    RAG_FETCH_K: int = 20
    RAG_MIN_SCORE: float = 0.2
    COMPARE_MIN_SCORE: float = 0.35

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DB: str = "pratibha"
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DSN: str | None = None
    # Managed hosts (Railway/Render/Supabase/Neon) expose a single connection
    # string. When present it wins and is parsed into the PG_* fields below so
    # every asyncpg.connect() call site keeps working unchanged.
    DATABASE_URL: str | None = None
    # Force TLS for the Postgres connection. Auto-enabled when the connection
    # string requests it (e.g. ?sslmode=require), which managed external
    # endpoints typically need. Internal/private networking can leave this off.
    PG_SSL: bool = False

    @field_validator("OPENAI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY", mode="before")
    @classmethod
    def normalize_keys(cls, v):
        if v is None:
            return None
        s = str(v).strip()
        # Treat empty/comment placeholders as unset.
        if not s or s.startswith("#"):
            return None
        return s

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="after")
    def _hydrate_pg_from_url(self):
        """Populate discrete PG_* fields from a single connection string.

        Precedence: DATABASE_URL > PG_DSN. Only fields present in the URL
        override the defaults, so partial URLs degrade gracefully. Scheme
        suffixes such as ``postgresql+psycopg`` are tolerated.
        """
        url = (self.DATABASE_URL or self.PG_DSN or "").strip()
        if not url:
            return self
        parsed = urlparse(url)
        if parsed.hostname:
            self.PG_HOST = parsed.hostname
        if parsed.port:
            self.PG_PORT = parsed.port
        if parsed.username:
            self.PG_USER = unquote(parsed.username)
        if parsed.password:
            self.PG_PASSWORD = unquote(parsed.password)
        db = (parsed.path or "").lstrip("/")
        if db:
            self.PG_DB = db
        sslmode = (parse_qs(parsed.query).get("sslmode", [""])[0] or "").lower()
        if sslmode in {"require", "verify-ca", "verify-full", "prefer", "allow"}:
            self.PG_SSL = True
        return self

    def asyncpg_kwargs(self) -> dict:
        """Connection kwargs shared by every asyncpg.connect() call site."""
        kwargs: dict = {
            "host": self.PG_HOST,
            "port": self.PG_PORT,
            "user": self.PG_USER,
            "password": self.PG_PASSWORD,
            "database": self.PG_DB,
        }
        if self.PG_SSL:
            # Managed providers frequently present certs that don't chain to the
            # system trust store; encrypt without strict verification (fine for
            # a single-tenant MVP, avoids a class of opaque TLS failures).
            ctx = _ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = _ssl.CERT_NONE
            kwargs["ssl"] = ctx
        return kwargs

    def chat_provider(self) -> str:
        if self.OPENROUTER_API_KEY:
            return "openrouter"
        if self.GROQ_API_KEY:
            return "groq"
        if self.OPENAI_API_KEY:
            return "openai"
        return "none"

    def effective_default_model(self) -> str:
        if self.chat_provider() == "openrouter":
            model = (self.DEFAULT_MODEL or "").strip()
            if model.startswith("openrouter/"):
                return model
            return self.OPENROUTER_MODEL
        return self.DEFAULT_MODEL

settings = Settings()
