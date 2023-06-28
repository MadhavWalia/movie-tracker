from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # MongoDB Settings
    def __hash__(self) -> int:
        return 1

    mongo_connection_string: str
    mongo_database_name: str

    class Config:
        env_file = ".env"


@lru_cache()
def settings_instance():
    """
    Creates a singleton instance of Fast API Settings Dependency
    """
    return Settings()
