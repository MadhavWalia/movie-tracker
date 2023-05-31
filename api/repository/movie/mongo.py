from typing import List, Optional

import motor.motor_asyncio

from api.entities.movie import Movie
from api.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)


class MongoMovieRepository(MovieRepository):
    """
    MongoMovieRepository is a repository pattern implementation that stores movies in a MongoDB database.

    """

    def __init__(
        self,
        connection_string: str = "mongodb://127.0.0.1:27017",
        database: str = "movie_track_db",
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        # Movie collection which holds our movie documents
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
        result = await self._movies.update_one(
            {"id": movie.id},
            {
                "$set": {
                    "id": movie.id,
                    "title": movie.title,
                    "description": movie.description,
                    "released_year": movie.released_year,
                    "watched": movie.watched,
                }
            },
            upsert=True,
        )

    async def get_by_id(self, movie_id: str) -> Optional[Movie]:
        document = await self._movies.find_one({"id": movie_id})
        if document:
            return Movie(
                movie_id=document.get("id"),
                title=document.get("title"),
                description=document.get("description"),
                released_year=document.get("released_year"),
                watched=document.get("watched"),
            )
        return None

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> List[Movie]:
        return_value: List[Movie] = []
        # Get cursor to iterate over documents
        document_cursor = self._movies.find({"title": title}).skip(skip).limit(limit)
        async for document in document_cursor:
            return_value.append(
                Movie(
                    movie_id=document.get("id"),
                    title=document.get("title"),
                    description=document.get("description"),
                    released_year=document.get("released_year"),
                    watched=document.get("watched"),
                )
            )
        return return_value

    async def delete(self, movie_id: str):
        await self._movies.delete_one({"id": movie_id})

    async def update(self, movie_id: str, update_parameters: dict):
        if "id" in update_parameters.keys():
            raise RepositoryException("Cannot update movie id")
        result = await self._movies.update_one(
            {"id": movie_id}, {"$set": update_parameters}
        )
        if result.modified_count == 0:
            raise RepositoryException(f"Movie with id {movie_id} not updated")
