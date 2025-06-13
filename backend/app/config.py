from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    api_prefix_b1: str = '/api/b1'
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR / 'db.sqlite3'}"
    db_echo: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
