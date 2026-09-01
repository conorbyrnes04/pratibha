"""Pydantic settings. Edit values in `.env`.
"""
import ssl as _ssl
from urllib.parse import parse_qs, unquote, urlparse

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    # OpenAI key is retained for RAG embeddings only (chat runs on OpenRouter).
    OPENAI_API_KEY: str | None = None
    # Legacy: Groq is no longer used for chat. Kept so old .env files don't error.
    GROQ_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    # Cheap, fast, voice-capable default. Override in .env with any OpenRouter id.
    OPENROUTER_MODEL: str = "openrouter/anthropic/claude-haiku-4.5"
    OPENROUTER_SITE_URL: str | None = None
    OPENROUTER_APP_NAME: str = "Pratibha"
    DEFAULT_MODEL: str = "openrouter/anthropic/claude-haiku-4.5"
    OPENAI_MODEL: str = "gpt-4o-mini"
    USE_RAG: bool = False
    # "pgvector" (legacy Supabase) or "convex" (rag_chunks vector index). Convex
    # rides the same deployment as auth/social; the /rag/* HTTP actions live on
    # the .convex.site origin derived from NEXT_PUBLIC_CONVEX_URL per environment.
    VECTOR_BACKEND: str = "pgvector"
    # Shared secret guarding the Convex /rag/* HTTP actions (also set in the
    # Convex deployment env). Required for the convex backend to read/ingest.
    RAG_INGEST_TOKEN: str | None = None
    # Chat must return well inside the client's patience. A fast model + a hard
    # per-request cap keeps the round trip under ~20s even on a cold backend.
    REQUEST_TIMEOUT_S: float = 18.0
    CHAT_MAX_TOKENS: int = 700
    MAX_RETRIES: int = 1
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    RAG_FETCH_K: int = 20
    RAG_MIN_SCORE: float = 0.2
    COMPARE_MIN_SCORE: float = 0.35

    # ---- Study chat cost controls (soft caps + model routing) ----
    # CHAT_DAILY_MAX: soft daily message cap per IP (or authenticated user id).
    #   0 disables. Exceeded → HTTP 429 with code "daily_cap".
    # CHAT_MODEL_SIMPLE: OpenRouter id for chat_mode=question / depth=simple
    #   (defaults to DEFAULT_MODEL / Haiku).
    # CHAT_MODEL_DEEP: OpenRouter id for explain|compare|practice / depth=deep
    #   (defaults to DEFAULT_MODEL; set e.g. openrouter/anthropic/claude-sonnet-4
    #   in .env when you want a stronger model for deep modes).
    # CHAT_SIMPLE_MAX_TOKENS: shorter completion budget for simple routing.
    CHAT_DAILY_MAX: int = 40
    CHAT_MODEL_SIMPLE: str = ""
    CHAT_MODEL_DEEP: str = ""
    CHAT_SIMPLE_MAX_TOKENS: int = 500

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DB: str = "pratibha"
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DSN: str | None = None
    # Managed hosts (Railway/Render/Neon) expose a single connection
    # string. When present it wins and is parsed into the PG_* fields below so
    # every asyncpg.connect() call site keeps working unchanged.
    DATABASE_URL: str | None = None
    # Force TLS for the Postgres connection. Auto-enabled when the connection
    # string requests it (e.g. ?sslmode=require), which managed external
    # endpoints typically need. Internal/private networking can leave this off.
    PG_SSL: bool = False

    # Optional auth backends. Convex is the new path; Supabase fields remain so
    # existing .env files and /health stay valid. Production default so Render
    # chat auth (F6) is on even if the dashboard env var was never set.
    NEXT_PUBLIC_CONVEX_URL: str | None = "https://giant-lapwing-264.convex.cloud"
    NEXT_PUBLIC_CONVEX_SITE_URL: str | None = None
    SUPABASE_URL: str | None = None
    SUPABASE_JWT_SECRET: str | None = None
    # Private Listen archive (never expose this key to the browser).
    SUPABASE_SERVICE_ROLE_KEY: str | None = None
    LISTEN_BUCKET: str = "listen"
    # Listen (ElevenLabs). Voice rooms are selected in app/tts.py.
    ELEVENLABS_API_KEY: str | None = None

    @field_validator(
        "OPENAI_API_KEY",
        "GROQ_API_KEY",
        "OPENROUTER_API_KEY",
        "ELEVENLABS_API_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
        "RAG_INGEST_TOKEN",
        mode="before",
    )
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
            # PgBouncer transaction pooling rejects prepared statements.
            "statement_cache_size": 0,
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
        # Chat is OpenRouter-only. Groq/OpenAI are no longer chat providers.
        return "openrouter" if self.OPENROUTER_API_KEY else "none"

    def effective_default_model(self) -> str:
        model = (self.DEFAULT_MODEL or "").strip()
        if model.startswith("openrouter/"):
            return model
        # Any non-OpenRouter id (legacy Groq/OpenAI) falls back to the OpenRouter default.
        return self.OPENROUTER_MODEL

    def _normalize_openrouter_model(self, model: str | None) -> str:
        m = (model or "").strip()
        if not m:
            return self.effective_default_model()
        return m if m.startswith("openrouter/") else f"openrouter/{m}"

    def effective_chat_model_simple(self) -> str:
        """Cheaper/faster model for open questions (defaults to DEFAULT_MODEL)."""
        return self._normalize_openrouter_model(self.CHAT_MODEL_SIMPLE) if (self.CHAT_MODEL_SIMPLE or "").strip() else self.effective_default_model()

    def effective_chat_model_deep(self) -> str:
        """Stronger model for explain/compare/practice (defaults to DEFAULT_MODEL)."""
        return self._normalize_openrouter_model(self.CHAT_MODEL_DEEP) if (self.CHAT_MODEL_DEEP or "").strip() else self.effective_default_model()

settings = Settings()
