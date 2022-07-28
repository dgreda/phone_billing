from fastapi import FastAPI

from app.containers import AppContainer
from app.db import init_db
from app.domain.models import PhoneCall, User
from app.endpoints import router


def create_app() -> FastAPI:
    container = AppContainer()

    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    init_db()
