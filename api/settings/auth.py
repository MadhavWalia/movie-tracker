from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # MongoDB Settings
    def __hash__(self) -> int:
        return 1

    mongo_connection_string: str = Field(
        "mongodb://127.0.0.1:27017",
        title="MongoDB Connection String",
        description="The connection string to connect to MongoDB",
        env="MONGODB_CONNECTION_STRING",
    )

    mongo_database_name: str = Field(
        "auth_db",
        title="MongoDB Auth Database Name",
        description="The name of the database for movies to use in MongoDB",
        env="MONGODB_DATABASE_NAME",
    )


@lru_cache()
def settings_instance():
    """
    Creates a singleton instance of Fast API Settings Dependency
    """
    return Settings()


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

    @classmethod
    def get_settings(cls):
        return cls()
