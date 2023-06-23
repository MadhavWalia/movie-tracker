"""
Token Refresh:

URL: POST www.example.com/auth/v1/refresh
User Profile Retrieval:

URL: GET www.example.com/auth/v1/profile
Password Reset:

URL: POST www.example.com/auth/v1/reset-password
Password Change:

URL: POST www.example.com/auth/v1/change-password
User Account Deactivation:

URL: DELETE www.example.com/auth/v1/account
Logout:

URL: POST www.example.com/auth/v1/logout

"""

from functools import lru_cache
from http import HTTPStatus
import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from api.dto.auth import AccessTokenResponse, UserRegisteredResponse
from api.dto.detail import DetailResponse
from api.entities.auth import AuthUser
from api.repository.auth.abstractions import AuthUserRepository
from api.repository.auth.mongo import MongoAuthRepository

from api.settings.auth import Settings, settings_instance
from api.utils.auth import create_access_token


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@lru_cache()
def auth_repository(settings: Settings = Depends(settings_instance)):
    """
    Creates a singleton instance of Auth Repository Dependency
    """
    return MongoAuthRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


@router.post(
    "/register",
    responses={
        HTTPStatus.CREATED.value: {"model": UserRegisteredResponse},
        HTTPStatus.BAD_REQUEST.value: {"model": DetailResponse},
    },
)
async def register_user(
    user: OAuth2PasswordRequestForm = Depends(),
    repo: AuthUserRepository = Depends(auth_repository),
):
    """
    Register a user
    """

    # Check if the username already exists
    if await repo.get_user(username=user.username) is not None:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=jsonable_encoder(DetailResponse(message="User already exists")),
        )

    # Create a new user
    user_id = str(uuid.uuid4())

    await repo.create(
        authuser=AuthUser(
            user_id=user_id,
            username=user.username,
            password=user.password,
        )
    )

    # Return the user id
    return UserRegisteredResponse(user_id=user_id)


@router.post(
    "/login",
    responses={
        HTTPStatus.OK.value: {"model": AccessTokenResponse},
        HTTPStatus.UNAUTHORIZED.value: {"model": DetailResponse},
    },
)
async def login_user(
    user: OAuth2PasswordRequestForm = Depends(),
    repo: AuthUserRepository = Depends(auth_repository),
):
    """
    Login a user
    """

    # Authenticate the username and password
    try:
        await repo.verify_account(
            username=user.username,
            password=user.password,
        )

    except Exception as e:
        raise e
        # return JSONResponse(
        #     status_code=HTTPStatus.UNAUTHORIZED,
        #     content=jsonable_encoder(DetailResponse(message=str(e))),
        # )

    # Generate the access token
    access_token = create_access_token(username=user.username)

    # Return the access token
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=jsonable_encoder(
            AccessTokenResponse(access_token=access_token, token_type="bearer")
        ),
    )
