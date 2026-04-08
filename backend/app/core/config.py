from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-Based Early Warning System API"
    app_env: str = "development"
    database_url: str = "sqlite:///./ews.db"
    cors_origins: List[str] | str = ["http://localhost:5173", "http://127.0.0.1:5173"]

    auth_enabled: bool = False
    read_only_demo: bool = True
    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    default_admin_email: str = "admin@example.com"
    default_admin_password: str = "Admin@123"

    project_root: Path = Path(__file__).resolve().parents[3]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
