"""Application configuration using Pydantic settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    app_name: str = "WfL Dashboard API"
    database_url: str = "sqlite:///./data.db"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
