from typing import List, Optional

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from app.domain.entities.InvoiceBase import InvoiceBase
from app.domain.entities.User import User


class Invoice(InvoiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="invoices")
    identifier: str = Field(index=True, sa_column=Column(String(), unique=True))
    calls: List["Call"] = Relationship(back_populates="invoice")  # type: ignore # noqa
