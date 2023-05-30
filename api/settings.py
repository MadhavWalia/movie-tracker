from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # MongoDB Settings
    mongo_connection_string: str = Field(
        "mongodb://127.0.0.1:27017",
        title="MongoDB Connection String",
        description="The connection string to connect to MongoDB",
        env="MONGODB_CONNECTION_STRING",
    )

    mongo_database_name: str = Field(
        "movie_track_db",
        title="MongoDB Moviees Database Name",
        description="The name of the database for movies to use in MongoDB",
        env="MONGODB_DATABASE_NAME",
    )
