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

    async def get_username(self, username: str) -> Optional[User]:
        """
        Returns a user by username or None if not found

        """
        return NotImplementedError

    def verify_account(self, user: User):
        """
        Verifies a password against a hash

        """
        return NotImplementedError

    async def delete(self, username: str):
        """
        Deletes a user by username

        Raises RepositoryException on failure

        """
        return NotImplementedError

    async def update(self, user: User, update_parameters: dict):
        """
        Updates a user's profile

        Raises RepositoryException on failure

        """
        return NotImplementedError
