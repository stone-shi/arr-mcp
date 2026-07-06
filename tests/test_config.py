import os
import pytest
from pydantic import ValidationError
from config import Settings


class TestSettings:
    def test_settings_loads_from_env(self, monkeypatch):
        monkeypatch.setenv("LIDARR_URL", "http://lidarr:8686")
        monkeypatch.setenv("LIDARR_API_KEY", "lidarr-key")
        monkeypatch.setenv("RADARR_URL", "http://radarr:7878")
        monkeypatch.setenv("RADARR_API_KEY", "radarr-key")
        monkeypatch.setenv("SONARR_URL", "http://sonarr:8989")
        monkeypatch.setenv("SONARR_API_KEY", "sonarr-key")
        monkeypatch.setenv("ARR_SSL_VERIFY", "False")
        monkeypatch.setenv("MCP_TRANSPORT", "stdio")
        monkeypatch.setenv("MCP_HOST", "0.0.0.0")
        monkeypatch.setenv("MCP_PORT", "8000")

        settings = Settings()
        assert settings.lidarr_url == "http://lidarr:8686"
        assert settings.lidarr_api_key == "lidarr-key"
        assert settings.radarr_url == "http://radarr:7878"
        assert settings.radarr_api_key == "radarr-key"
        assert settings.sonarr_url == "http://sonarr:8989"
        assert settings.sonarr_api_key == "sonarr-key"
        assert settings.arr_ssl_verify is False
        assert settings.mcp_transport == "stdio"
        assert settings.mcp_host == "0.0.0.0"
        assert settings.mcp_port == 8000

    def test_settings_missing_required_fields(self, monkeypatch):
        monkeypatch.delenv("LIDARR_URL", raising=False)
        monkeypatch.delenv("LIDARR_API_KEY", raising=False)
        monkeypatch.delenv("RADARR_URL", raising=False)
        monkeypatch.delenv("RADARR_API_KEY", raising=False)
        monkeypatch.delenv("SONARR_URL", raising=False)
        monkeypatch.delenv("SONARR_API_KEY", raising=False)
        with pytest.raises(ValidationError):
            Settings(_env_file=None)

    def test_settings_ssl_verify_true(self, monkeypatch):
        monkeypatch.setenv("LIDARR_URL", "http://lidarr:8686")
        monkeypatch.setenv("LIDARR_API_KEY", "lidarr-key")
        monkeypatch.setenv("RADARR_URL", "http://radarr:7878")
        monkeypatch.setenv("RADARR_API_KEY", "radarr-key")
        monkeypatch.setenv("SONARR_URL", "http://sonarr:8989")
        monkeypatch.setenv("SONARR_API_KEY", "sonarr-key")
        monkeypatch.setenv("ARR_SSL_VERIFY", "True")

        settings = Settings()
        assert settings.arr_ssl_verify is True

    def test_settings_default_values(self, monkeypatch):
        monkeypatch.setenv("LIDARR_URL", "http://lidarr:8686")
        monkeypatch.setenv("LIDARR_API_KEY", "lidarr-key")
        monkeypatch.setenv("RADARR_URL", "http://radarr:7878")
        monkeypatch.setenv("RADARR_API_KEY", "radarr-key")
        monkeypatch.setenv("SONARR_URL", "http://sonarr:8989")
        monkeypatch.setenv("SONARR_API_KEY", "sonarr-key")

        settings = Settings()
        assert settings.arr_ssl_verify is False
        assert settings.mcp_transport == "stdio"
        assert settings.mcp_host == "0.0.0.0"
        assert settings.mcp_port == 8000

    def test_settings_custom_transport(self, monkeypatch):
        monkeypatch.setenv("LIDARR_URL", "http://lidarr:8686")
        monkeypatch.setenv("LIDARR_API_KEY", "lidarr-key")
        monkeypatch.setenv("RADARR_URL", "http://radarr:7878")
        monkeypatch.setenv("RADARR_API_KEY", "radarr-key")
        monkeypatch.setenv("SONARR_URL", "http://sonarr:8989")
        monkeypatch.setenv("SONARR_API_KEY", "sonarr-key")
        monkeypatch.setenv("MCP_TRANSPORT", "sse")
        monkeypatch.setenv("MCP_HOST", "127.0.0.1")
        monkeypatch.setenv("MCP_PORT", "9000")

        settings = Settings()
        assert settings.mcp_transport == "sse"
        assert settings.mcp_host == "127.0.0.1"
        assert settings.mcp_port == 9000
