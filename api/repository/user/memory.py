from typing import List, Optional

from passlib.context import CryptContext
from pydantic import ValidationError

from api.entities.user import User
from api.repository.user.abstractions import RepositoryException, UserRepository


class MemoryUserRepository(UserRepository):
    """

    MemoryUserRepository is a repository pattern implementation that stores users in memory.

    """

    def __init__(self):
        self._storage = {}
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    async def create(self, user: User):
        user._password = self._pwd_context.hash(user.password)
        for stored_user in self._storage.values():
            if user.username == stored_user.username:
                raise RepositoryException(
                    f"User with username {user.username} already exists"
                )
        self._storage[user.user_id] = user

    async def get_user(self, username: str) -> Optional[User]:
        for user in self._storage.values():
            if user.username == username:
                return user
        return None

    async def verify_account(self, user: User) -> bool:
        stored_user = await self.get_user(user.username)
        if stored_user is None:
            raise RepositoryException(f"User with username {user.username} not found")

        if not self._pwd_context.verify(user.password, stored_user.password):
            raise RepositoryException("Invalid password")
        else:
            return True

    async def delete(self, username: str):
        for stored_user in self._storage.values():
            if username == stored_user.username:
                self._storage.pop(stored_user.user_id, None)
                return

    async def update(self, user: User, update_parameters: dict):
        try:
            await self.verify_account(user)
        except RepositoryException as e:
            raise e

        stored_user = await self.get_user(user.username)
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
