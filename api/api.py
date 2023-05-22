from fastapi import FastAPI

from api.handlers import demo


def create_app():
    app = FastAPI(docs_url="/")

    # Routers
    app.include_router(demo.router)

    return app
