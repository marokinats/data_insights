"""Tests for configuration."""

from app.core.config import settings


def test_settings_loaded() -> None:
    """Test that settings are loaded correctly."""
    assert settings.APP_NAME == "Data Insights API"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.MAX_UPLOAD_SIZE > 0
    assert settings.MONTHS_TO_DAYS_MULTIPLIER == 30.42


def test_cors_origins() -> None:
    """Test CORS origins are configured."""
    assert len(settings.BACKEND_CORS_ORIGINS) > 0
    assert any("localhost" in origin for origin in settings.BACKEND_CORS_ORIGINS)
