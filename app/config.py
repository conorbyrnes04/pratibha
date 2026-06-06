"""Pydantic settings. Edit values in `.env`.
"""
from pydantic import field_validator
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
