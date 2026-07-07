from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Valthera AI Engine")
    app_version: str = Field(default="0.2.0")
    environment: str = Field(default="development")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.1", alias="OLLAMA_MODEL")
    ollama_timeout_seconds: int = Field(default=30, alias="OLLAMA_TIMEOUT_SECONDS", gt=0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
