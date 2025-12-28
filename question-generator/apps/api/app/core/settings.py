from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

API_DIR = Path(__file__).resolve().parents[2]

DB_PATH = API_DIR / "qgen.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    database_url: str = f"sqlite:////{DB_PATH}"
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")


settings = Settings()
