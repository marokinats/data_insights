"""Application configuration."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

    # App
    APP_NAME: str = "Data Insights API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Env
    ENVIRONMENT: Literal["development", "production"] = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set[str] = {".csv"}
    UPLOAD_DIR: str = "uploads"

    # Session
    SESSION_EXPIRE_MINUTES: int = 60

    # Data Processing
    MONTHS_TO_DAYS_MULTIPLIER: float = 30.44  # Average days per month


settings = Settings()
