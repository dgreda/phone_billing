from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.models.User import User


class PhoneCall(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="phone_calls")
    target_number: int
    start_timestamp_utc: datetime
    end_timestamp_utc: datetime
    duration_in_minutes: int
