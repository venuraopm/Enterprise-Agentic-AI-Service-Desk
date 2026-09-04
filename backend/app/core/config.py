from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Enterprise AI Service Desk"
    app_version: str = "1.0.0"
    app_description: str = "Enterprise AI Service Desk powered by Agentic AI"
    log_level: str = "INFO"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    database_url: str = "sqlite:///./database/servicedesk.db"
    chroma_path: str = "../database/chroma_db"
    kb_dir: str = "../knowledgebase"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2"

    langsmith_tracing: bool = False
    langsmith_api_key: str = ""
    langsmith_project: str = "ai-servicedesk"

    azure_tenant_id: str = ""
    azure_client_id: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = ""

    @field_validator("cors_origins", mode="before")
    @classmethod
    def strip_origins(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
