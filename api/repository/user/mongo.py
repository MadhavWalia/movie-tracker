from typing import List, Optional

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError
from passlib.context import CryptContext

from api.entities.user import User
from api.repository.user.abstractions import (UserRepository,
                                               RepositoryException)


class MongoUserRepository(UserRepository):
    """
    MongoUserRepository is a repository pattern implementation that stores users in a MongoDB database.

    """

    def __init__(
        self,
        connection_string: str = "mongodb://127.0.0.1:27017",
        database: str = "user_db",
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        # User collection which holds our user documents
        self._users = self._database["users"]
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    async def create(self, user: User):
        await self._users.create_index("username", unique=True)
        hashed_password = self._pwd_context.hash(user.password)
        try:
            result = await self._users.insert_one(
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "password": hashed_password,
                }
            )
        except DuplicateKeyError:
            raise RepositoryException(f"User with username {user.username} already exists")

    async def get_user(self, username: str) -> Optional[User]:
        document = await self._users.find_one({"username": username})
        if document:
            return User(
                user_id=document.get("user_id"),
                username=document.get("username"),
                password=document.get("password"),
            )
        return None

    async def verify_account(self, user: User):
        document = await self._users.find_one({"username": user.username})
        if document:
            if self._pwd_context.verify(user.password, document.get("password")):
                return True
            else:
                raise RepositoryException(f"Password for user {user.username} is incorrect")
        else:
            raise RepositoryException(f"User with username {user.username} does not exist")

    async def delete(self, username: str):
        await self._users.delete_one({"username": username})

    async def update(self, user: User, update_parameters: dict):
        if "user_id" in update_parameters.keys():
            raise RepositoryException("Cannot update user id")
        
        try:
            await self.verify_account(user)
        except RepositoryException as e:
            raise e
        
        if "password" in update_parameters.keys():
            update_parameters["password"] = self._pwd_context.hash(update_parameters["password"])
        result = await self._movies.update_one(
            {"user_id": user.user_id}, {"$set": update_parameters}
        )
        
        if result.modified_count == 0:
            raise RepositoryException(f"User with id {user.username} not updated")
