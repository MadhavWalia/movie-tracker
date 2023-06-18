from fastapi import FastAPI
from api.handlers import demo, movie_v1
from starlette_prometheus import metrics
from api.middleware import middleware


def create_app():
    app = FastAPI(docs_url="/", middleware=middleware)

    # Routers
    # app.include_router(demo.router)
    app.include_router(movie_v1.router)
    app.add_route("/metrics/", metrics)

    return app
