from abc import ABC
from typing import List, TypeVar

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

    def persist_all(self, entities: List[T]) -> List[T]:
        for entity in entities:
            self.session.add(entity)

        self.session.commit()

        for entity in entities:
            self.session.refresh(entity)

        return entities
