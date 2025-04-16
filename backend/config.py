from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class EnvironSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    GEMINI_API_KEY: str


@lru_cache
def get_env_settings() -> EnvironSettings:
    """
    Get the environment settings.
    """
    return EnvironSettings()
