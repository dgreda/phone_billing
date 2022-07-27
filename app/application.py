from fastapi import FastAPI

from . import endpoints
from .containers import AppContainer


def create_app() -> FastAPI:
    container = AppContainer()

    app = FastAPI()
    app.include_router(endpoints.router)
    return app


app = create_app()
