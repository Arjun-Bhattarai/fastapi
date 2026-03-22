from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    #APP_NAME: str
    #APP_ENV: str
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    #ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",  # points to src/.env
        extra="ignore"
    )

config = Settings()