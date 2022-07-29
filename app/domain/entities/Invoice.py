from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.User import User


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="invoices")
    identifier: str = Field(index=True)
    billing_month: int
    billing_year: int
    calls: List["Call"] = Relationship(back_populates="invoice")  # type: ignore
