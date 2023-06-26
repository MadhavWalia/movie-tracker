from functools import lru_cache
from fastapi import Depends, HTTPException
from http import HTTPStatus
from jose import jwt, JWTError
from datetime import datetime
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette_prometheus import PrometheusMiddleware

from api.middleware.protected_routes import PROTECTED_ROUTES
from api.repository.auth.mongo import MongoAuthRepository
from api.settings.auth import settings_instance
from api.utils.auth import decode_token


@lru_cache()
def auth_repository():
    """
    Creates a singleton instance of Auth Repository Dependency
    """
    settings = settings_instance()
    return MongoAuthRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


class AuthenticatedMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.repo = auth_repository()

    async def dispatch(self, request: Request, call_next):
        # Check if the route requires protection
        if request.url.path in PROTECTED_ROUTES:
            # Check if the request has an Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content={"message": "Invalid Authorization header"},
                )

            # Extracting the token from the header
            token = auth_header.split(" ")[1]

            # Decoding the token
            try:
                payload = decode_token(token)
                username: str = payload.get("sub")
                expiry: int = payload.get("exp")

                # Checking if the token is expired
                if (
                    expiry is None
                    or datetime.utcfromtimestamp(expiry) < datetime.utcnow()
                ):
                    return JSONResponse(
                        status_code=HTTPStatus.UNAUTHORIZED,
                        content={"message": "Token expired"},
                    )

                # Checking if username is there in the authe database
                if await self.repo.get_user(username=username) is None:
                    return JSONResponse(
                        status_code=HTTPStatus.UNAUTHORIZED,
                        content={"message": "Invalid token"},
                    )

            except JWTError:
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content={"message": "Invalid token"},
                )

        response = await call_next(request)
        return response


# The middleware is added to the app in api\api.py:
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(PrometheusMiddleware),
    # Middleware(HTTPSRedirectMiddleware),
    Middleware(AuthenticatedMiddleware),
]
