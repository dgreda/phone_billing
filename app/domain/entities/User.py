from typing import List, Optional

from sqlmodel import Field, Relationship

from app.domain.entities.UserBase import UserBase


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    calls: List["Call"] = Relationship(back_populates="user")  # type: ignore # noqa
    invoices: List["Invoice"] = Relationship(back_populates="user")  # type: ignore # noqa
