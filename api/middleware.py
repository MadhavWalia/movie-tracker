from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette_prometheus import PrometheusMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware


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
    Middleware(HTTPSRedirectMiddleware)
]
