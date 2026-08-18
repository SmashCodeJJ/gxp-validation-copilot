from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GxP Validation Copilot"
    app_version: str = "1.0.0"
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
    api_host: str = "0.0.0.0"
    api_port: int = Field(
        default=8000,
        ge=1,
        le=65535,
    )
    api_workers: int = Field(
        default=1,
        ge=1,
        le=8,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
