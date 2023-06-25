from typing import List, Optional

from passlib.context import CryptContext
from pydantic import ValidationError

from api.entities.auth import AuthUser
from api.repository.auth.abstractions import RepositoryException, AuthUserRepository


class MemoryAuthRepository(AuthUserRepository):
    """

    MemoryAuthRepository is a repository pattern implementation that stores authusers in memory.

    """

    def __init__(self):
        self._storage = {}
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    async def create(self, authuser: AuthUser):
        authuser._password = self._pwd_context.hash(authuser.password)
        for stored_user in self._storage.values():
            if authuser.username == stored_user.username:
                raise RepositoryException(
                    f"User with username {authuser.username} already exists"
                )
        self._storage[authuser.user_id] = authuser

    async def get_user(self, username: str) -> Optional[AuthUser]:
        for authuser in self._storage.values():
            if authuser.username == username:
                return authuser
        return None

    async def verify_account(self, username: str, password: str) -> bool:
        stored_user = await self.get_user(username)
        if stored_user is None:
            raise RepositoryException(f"User with username {username} not found")

        if not self._pwd_context.verify(password, stored_user.password):
            raise RepositoryException("Invalid password")
        else:
            return True

    async def delete(self, username: str):
        for stored_user in self._storage.values():
            if username == stored_user.username:
                self._storage.pop(stored_user.user_id, None)
                return

    async def update(self, authuser: AuthUser, update_parameters: dict):
        try:
            await self.verify_account(
                username=authuser.username, password=authuser.password
            )
        except RepositoryException as e:
            raise e

        stored_user = await self.get_user(authuser.username)
        for key, value in update_parameters.items():
            if key == "user_id":
                raise RepositoryException("Cannot update user id")

            if key == "password":
                if self._pwd_context.verify(value, stored_user.password):
                    raise RepositoryException(
                        "New password cannot be the same as the old one"
                    )
                value = self._pwd_context.hash(value)

            # Check that update parameters are fields from User Entity
            if hasattr(stored_user, key):
                setattr(stored_user, f"_{key}", value)
