from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GxP Validation Copilot"
    environment: str = "development"

    database_url: str

    openai_api_key: str
    openai_model: str = "gpt-5-mini"

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    semantic_top_k: int = Field(
        default=3,
        ge=1,
        le=20,
    )

    rag_requirement_limit: int = Field(
        default=3,
        ge=1,
        le=20,
    )

    rag_test_limit: int = Field(
        default=3,
        ge=1,
        le=20,
    )

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache # for recreating get_settings()
def get_settings() -> Settings:
    return Settings()