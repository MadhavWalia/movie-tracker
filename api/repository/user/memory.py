import itertools
from passlib.context import CryptContext
from typing import List, Optional

from api.entities.user import User
from api.repository.user.abstractions import UserRepository, RepositoryException


class MemoryMovieRepository(UserRepository):
    """

    MemoryUserRepository is a repository pattern implementation that stores users in memory.

    """

    def __init__(self):
        self._storage = {}
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create(self, user: User):
        hashed_password = self.pwd_context.hash(user.password)
        if user.username in self._storage:
            raise RepositoryException(f"User with username {user.username} already exists")
        self._storage[user.username] = user.copy(update={"password": hashed_password})

    async def get_username(self, username: str) -> Optional[User]:
        return self.users.get(username)
    
    async def verify_account(self, user: User):
        stored_user = self._storage.get(user.username)
        if stored_user is None:
            raise RepositoryException(f"User with username {user.username} not found")
        
        if self.pwd_context.verify(user.password, stored_user.password) is False:
            raise RepositoryException("Invalid password")
        else:
            return stored_user

    async def delete(self, username: str):
        self._storage.pop(username, None)

    async def update(self, user: User, update_parameters: dict):
        try:
            stored_user = self.verify_account(user)
        except RepositoryException as e:
            raise e
        
        for key, value in update_parameters.items():
            if key == "password" and value == stored_user.password:
                raise RepositoryException(f"New password cannot be the same as the old one")

            # Check that update parameters are fields from User Entity
            if hasattr(stored_user, key):
                setattr(stored_user, f"_{key}", value)
