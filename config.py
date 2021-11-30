from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    database_dsn: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()
