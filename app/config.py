"""Pydantic settings. Edit values in `.env`.
"""
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str
    DEFAULT_MODEL: str = "groq/llama-3.1-70b-versatile"
    OPENAI_MODEL: str = "gpt-4o-mini"
    USE_RAG: bool = False
    VECTOR_BACKEND: str = "pgvector"
    REQUEST_TIMEOUT_S: float = 20.0
    MAX_RETRIES: int = 2

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DB: str = "pratibha"
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DSN: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
