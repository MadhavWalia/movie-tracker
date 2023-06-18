from typing import List, Optional

from passlib.context import CryptContext
from pydantic import ValidationError

from api.entities.user import User
from api.repository.user.abstractions import (RepositoryException,
                                              UserRepository)


class MemoryUserRepository(UserRepository):
    """

    MemoryUserRepository is a repository pattern implementation that stores users in memory.

    """

    def __init__(self):
        self._storage = {}
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    async def create(self, user: User):
        user._password = self._pwd_context.hash(user.password)
        if user.username in self._storage:
            raise RepositoryException(
                f"User with username {user.username} already exists"
            )
        self._storage[user.username] = user.password

    async def get_user(self, username: str) -> Optional[User]:
        if username not in self._storage:
            return None
        return User(username=username, password=self._storage.get(username))

    async def verify_account(self, user: User) -> bool:
        stored_user = await self.get_user(user.username)
        if stored_user is None:
            raise RepositoryException(f"User with username {user.username} not found")

        if not self._pwd_context.verify(user.password, stored_user.password):
            raise RepositoryException("Invalid password")
        else:
            return True

    async def delete(self, username: str):
        self._storage.pop(username, None)

    async def update(self, user: User, update_parameters: dict):
        try:
            stored_user = await self.verify_account(user)
        except RepositoryException as e:
            raise e

        for key, value in update_parameters.items():
            if key == "username":
                self._storage[value] = self._storage.pop(user.username)
                user._username = value

            if key == "password":
                if value == user.password:
                    raise RepositoryException(
                        f"New password cannot be the same as the old one"
                    )
                value = self._pwd_context.hash(value)
                self._storage[user.username] = value
