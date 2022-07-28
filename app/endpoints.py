from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.containers import AppContainer

router = APIRouter()


@router.get("/")
@inject
def read_root(
    default_greeting: str = Depends(
        Provide[AppContainer.config.default.greeting]
    ),
):
    return {"message": default_greeting}
