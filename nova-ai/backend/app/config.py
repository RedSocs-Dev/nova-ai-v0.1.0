from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    name: str = "NOVA AI"
    database_path: str = "./data/nova.sqlite3"
    provider: str = "ollama"  # ollama or openai_compatible
    model: str = "llama3.2"
    base_url: str = "http://localhost:11434"
    api_key: str = ""
    timeout_seconds: float = 90
    max_input_chars: int = 20_000
    memory_enabled: bool = True
    cors_origins: str = "http://localhost:8000"
    model_config = SettingsConfigDict(env_prefix="NOVA_", env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
