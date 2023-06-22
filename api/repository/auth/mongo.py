from typing import List, Optional

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError
from passlib.context import CryptContext

from api.entities.auth import AuthUser
from api.repository.auth.abstractions import AuthUserRepository, RepositoryException


class MongoAuthRepository(AuthUserRepository):
    """
    MongoUserRepository is a repository pattern implementation that stores authusers in a MongoDB database.

    """

    def __init__(
        self,
        connection_string: str = "mongodb://127.0.0.1:27017",
        database: str = "auth_db",
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        # Auth collection which holds our auth documents
        self._auth = self._database["auth"]
        self._pwd_context = CryptContext(schemes=["bcrypt"])

    async def create(self, authuser: AuthUser):
        await self._auth.create_index("username", unique=True)
        hashed_password = self._pwd_context.hash(authuser.password)
        try:
            result = await self._auth.insert_one(
                {
                    "user_id": authuser.user_id,
                    "username": authuser.username,
                    "password": hashed_password,
                }
            )
        except DuplicateKeyError:
            raise RepositoryException(
                f"User with username {authuser.username} already exists"
            )

    async def get_user(self, username: str) -> Optional[AuthUser]:
        document = await self._auth.find_one({"username": username})
        if document:
            return AuthUser(
                user_id=document.get("user_id"),
                username=document.get("username"),
                password=document.get("password"),
            )
        return None

    async def verify_account(self, authuser: AuthUser):
        document = await self._auth.find_one({"username": authuser.username})
        if document:
            if self._pwd_context.verify(authuser.password, document.get("password")):
                return True
            else:
                raise RepositoryException(
                    f"Password for user {authuser.username} is incorrect"
                )
        else:
            raise RepositoryException(
                f"User with username {authuser.username} does not exist"
            )

    async def delete(self, username: str):
        await self._auth.delete_one({"username": username})

    async def update(self, authuser: AuthUser, update_parameters: dict):
        if "user_id" in update_parameters.keys():
            raise RepositoryException("Cannot update user id")

        try:
            await self.verify_account(authuser)
        except RepositoryException as e:
            raise e

        stored_user = await self.get_user(authuser.username)
        if "password" in update_parameters.keys():
            if self._pwd_context.verify(
                update_parameters["password"], stored_user.password
            ):
                raise RepositoryException(
                    "New password cannot be the same as the old password"
                )
            update_parameters["password"] = self._pwd_context.hash(
                update_parameters["password"]
            )

        result = await self._auth.update_one(
            {"user_id": authuser.user_id}, {"$set": update_parameters}
        )

        if result.modified_count == 0:
            raise RepositoryException(f"User with id {authuser.username} not updated")
