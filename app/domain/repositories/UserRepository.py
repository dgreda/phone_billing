from app.domain.entities.CreateUserRequest import CreateUserRequest
from app.domain.entities.User import User
from app.domain.exceptions import UserNotFound

from .AbstractRepository import AbstractRepository


class UserRepository(AbstractRepository):
    def find_or_fail(self, id: int) -> User:
        user = self.session.get(User, id)
        if user is None:
            raise UserNotFound(id)

        return user

    def persist_user(self, request: CreateUserRequest) -> User:
        user = User(
            country_code=request.country_code,
            number=request.number,
        )
        user = self.persist(user)

        return user
