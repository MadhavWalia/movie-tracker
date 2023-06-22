from fastapi import HTTPException
from http import HTTPStatus
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette_prometheus import PrometheusMiddleware

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
]
