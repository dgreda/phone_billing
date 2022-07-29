from typing import Optional

from sqlmodel import Field, Relationship

from app.domain.entities.CallBase import CallBase
from app.domain.entities.Invoice import Invoice
from app.domain.entities.User import User


class Call(CallBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="calls")
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoice.id")
    invoice: Optional[Invoice] = Relationship(back_populates="calls")
