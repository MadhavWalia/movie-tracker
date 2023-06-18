import abc
from typing import List, Optional

from api.entities.user import User


class RepositoryException(Exception):
    pass


class UserRepository(abc.ABC):
    async def create(self, user: User):
        """
        Creates a user profile and returns true on success

        Raises RepositoryException on failure

        """
        return NotImplementedError

    async def get_username(self, movie_id: str) -> Optional[User]:
        """
        Returns a user by username or None if not found

        """
        return NotImplementedError
    
    def verify_password(self, plain_password: str, hashed_password: str):
        """
        Verifies a password against a hash

        """
        return NotImplementedError

    async def delete(self, movie_id: str):
        """
        Deletes a user by username

        Raises RepositoryException on failure

        """
        return NotImplementedError

    async def update_username(self, movie_id: str, update_parameters: dict):
        """
        Updates a user's username

        Raises RepositoryException on failure

        """
        return NotImplementedError
