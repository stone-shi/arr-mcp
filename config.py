import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    lidarr_url: str = Field(..., alias="LIDARR_URL")
    lidarr_api_key: str = Field(..., alias="LIDARR_API_KEY")
    
    radarr_url: str = Field(..., alias="RADARR_URL")
    radarr_api_key: str = Field(..., alias="RADARR_API_KEY")
    
    sonarr_url: str = Field(..., alias="SONARR_URL")
    sonarr_api_key: str = Field(..., alias="SONARR_API_KEY")
    
    arr_ssl_verify: bool = Field(False, alias="ARR_SSL_VERIFY")
    
    mcp_transport: str = Field("stdio", alias="MCP_TRANSPORT")
    mcp_host: str = Field("0.0.0.0", alias="MCP_HOST")
    mcp_port: int = Field(8000, alias="MCP_PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
