from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.containers import AppContainer
from app.domain.exceptions import NotFound, NotUniqueError
from app.endpoints import router


def create_app() -> FastAPI:
    container = AppContainer()

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(router)
    return app


app = create_app()


@app.exception_handler(NotFound)
def not_found_exception_handler(request: Request, ex: NotFound):
    return JSONResponse(
        status_code=404,
        content={"error": str(ex)},
    )


@app.exception_handler(NotUniqueError)
def not_unique_error_exception_handler(request: Request, ex: NotUniqueError):
    return JSONResponse(
        status_code=409,
        content={"error": str(ex)},
    )
