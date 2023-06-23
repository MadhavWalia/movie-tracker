import abc
from typing import List, Optional

from api.entities.auth import AuthUser


class RepositoryException(Exception):
    pass


class AuthUserRepository(abc.ABC):
    async def create(self, authuser: AuthUser):
        """
        Creates a authuser profile and returns true on success

        Raises RepositoryException on failure

        """
        return NotImplementedError

    async def get_user(self, username: str) -> Optional[AuthUser]:
        """
        Returns a authuser by username or None if not found

        """
        return NotImplementedError

    def verify_account(self, username: str, password: str):
        """
        Verifies a password against a hash

        """
        return NotImplementedError

    async def delete(self, username: str):
        """
        Deletes a authuser by username

        Raises RepositoryException on failure

        """
        return NotImplementedError

    async def update(self, authuser: AuthUser, update_parameters: dict):
        """
        Updates a user's profile

        Raises RepositoryException on failure

        """
        return NotImplementedError
