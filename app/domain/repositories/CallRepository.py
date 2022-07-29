from typing import List

from sqlmodel import select

from app.domain.entities.Call import Call
from app.domain.entities.CreateCallRequest import CreateCallRequest
from app.domain.entities.User import User
from app.domain.exceptions import CallNotFound

from .AbstractRepository import AbstractRepository


class CallRepository(AbstractRepository):
    def find_or_fail(self, id: int) -> Call:
        call = self.session.get(Call, id)
        if call is None:
            raise CallNotFound(id)

        return call

    def find_by_user_id_paginated(
        self, user_id: int, offset: int, limit: int
    ) -> List[Call]:
        return self.session.exec(
            select(Call)
            .where(Call.user_id == user_id)
            .offset(offset)
            .limit(limit)
        ).all()

    def persist_call(self, request: CreateCallRequest, user: User) -> Call:
        call = Call(
            recipient_country_code=request.recipient_country_code,
            recipient_number=request.recipient_number,
            duration_in_minutes=request.duration_in_minutes,
            start_datetime_iso_8601=request.start_datetime_iso_8601,
            end_datetime_iso_8601=request.end_datetime_iso_8601,
            user_id=user.id,
        )
        call = self.persist(call)

        return call
