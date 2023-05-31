import abc
from typing import List, Optional

from api.entities.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    async def create(self, movie: Movie):
        """
        Creates a movie and returns true on success

        Raises RepositoryException on failure

        """
        return NotImplementedError

    async def get_by_id(self, movie_id: str) -> Optional[Movie]:
        """
        Returns a movie by id or None if not found

        """
        return NotImplementedError

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> List[Movie]:
        """
        Returns a list of movie sharing the same title

        """
        return NotImplementedError

    async def delete(self, movie_id: str):
        """
        Deletes a movie by id

        Raises RepositoryException on failure

        """
        return NotImplementedError

    async def update(self, movie_id: str, update_parameters: dict):
        """
        Updates a movie by id

        Raises RepositoryException on failure

        """
        return NotImplementedError
