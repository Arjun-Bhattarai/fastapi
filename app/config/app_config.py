from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(f"Looking for .env at: {BASE_DIR / '.env'}")
print(f"File exists: {(BASE_DIR / '.env').exists()}")

# This resolves to the directory containing app_config.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # goes up to fastapi/

class AppConfig(BaseSettings):
    app_name: str = "FastAPI"
    app_env: str = "development"
    database_url: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

@lru_cache()
def get_app_config() -> AppConfig:
    return AppConfig()