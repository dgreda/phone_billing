from abc import ABC
from typing import TypeVar

import sqlmodel

T = TypeVar("T")


class AbstractRepository(ABC):
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def persist(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)

        return entity
