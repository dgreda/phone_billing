from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: int = Field(index=True)
    phone_calls: List["PhoneCall"] = Relationship(back_populates="user")  # type: ignore
