from fastapi import FastAPI

from api.handlers import demo, movie_v1


def create_app():
    app = FastAPI(docs_url="/")

    # Routers
    # app.include_router(demo.router)
    app.include_router(movie_v1.router)

    return app
