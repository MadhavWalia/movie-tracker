import abc
from typing import List, Optional

from api.entities.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    def create(self, movie: Movie):
        """
        Creates a movie and returns true on success

        Raises RepositoryException on failure

        """
        return NotImplementedError

    def get_by_id(self, movie_id: str) -> Optional[Movie]:
        """
        Returns a movie by id or None if not found

        """
        return NotImplementedError

    def get_by_title(self, title: str) -> List[Movie]:
        """
        Returns a list of movie sharing the same title

        """
        return NotImplementedError

    def delete(self, movie_id: str):
        """
        Deletes a movie by id

        Raises RepositoryException on failure

        """
        return NotImplementedError

    def update(self, movie_id: str, update_parameters: dict):
        """
        Updates a movie by id

        Raises RepositoryException on failure

        """
        return NotImplementedError
