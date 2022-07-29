from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.containers import AppContainer
from app.domain.entities.Call import Call
from app.domain.entities.CallRead import CallRead
from app.domain.entities.CreateCallRequest import CreateCallRequest
from app.domain.entities.CreateUserRequest import CreateUserRequest
from app.domain.entities.Invoice import Invoice
from app.domain.entities.InvoiceRead import InvoiceRead
from app.domain.entities.User import User
from app.domain.entities.UserRead import UserRead
from app.domain.repositories import CallRepository, InvoiceRepository, UserRepository
from app.domain.services import InvoiceService

router = APIRouter()


@router.get("/")
@inject
def read_root(
    default_greeting: str = Depends(
        Provide[AppContainer.config.default.greeting]
    ),
):
    return {"message": default_greeting}


@router.get("/call/{call_id}", response_model=CallRead)
@inject
def get_call(
    call_id: int,
    call_repository: CallRepository = Depends(
        Provide[AppContainer.call_repository]
    ),
) -> Call:
    return call_repository.find_or_fail(call_id)


@router.get("/user/{user_id}", response_model=UserRead)
@inject
def get_user(
    user_id: int,
    user_repository: UserRepository = Depends(
        Provide[AppContainer.user_repository]
    ),
) -> User:
    return user_repository.find_or_fail(user_id)


@router.post("/user", status_code=201, response_model=UserRead)
@inject
def create_user(
    request: CreateUserRequest,
    user_repository: UserRepository = Depends(
        Provide[AppContainer.user_repository]
    ),
) -> User:
    return user_repository.persist_user(request)


@router.get("/user/{user_id}/phone_call", response_model=List[CallRead])
@inject
def get_user_phone_calls(
    user_id: int,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    call_repository: CallRepository = Depends(
        Provide[AppContainer.call_repository]
    ),
) -> List[Call]:
    return call_repository.find_by_user_id_paginated(
        user_id=user_id, offset=offset, limit=limit
    )


@router.post(
    "/user/{user_id}/phone_call", status_code=201, response_model=CallRead
)
@inject
def create_phone_call(
    user_id: int,
    request: CreateCallRequest,
    call_repository: CallRepository = Depends(
        Provide[AppContainer.call_repository]
    ),
    user_repository: UserRepository = Depends(
        Provide[AppContainer.user_repository]
    ),
) -> Call:
    user = user_repository.find_or_fail(user_id)
    call = call_repository.persist_call(request, user)

    return call


@router.post(
    "/user/{user_id}/invoice/{year}/{month}",
    status_code=201,
    response_model=InvoiceRead,
)
@inject
def create_invoice(
    user_id: int,
    year: int,
    month: int = Query(gte=1, lte=12),
    invoice_service: InvoiceService = Depends(
        Provide[AppContainer.invoice_service]
    ),
    user_repository: UserRepository = Depends(
        Provide[AppContainer.user_repository]
    ),
) -> Invoice:
    user = user_repository.find_or_fail(user_id)
    invoice = invoice_service.bill_and_create_invoice(
        user=user,
        billing_year=year,
        billing_month=month,
    )

    return invoice


@router.get("/invoice/{invoice_id}", response_model=InvoiceRead)
@inject
def get_invoice(
    invoice_id: int,
    invoice_repository: InvoiceRepository = Depends(
        Provide[AppContainer.invoice_repository]
    ),
) -> Invoice:
    return invoice_repository.find_or_fail(invoice_id)
