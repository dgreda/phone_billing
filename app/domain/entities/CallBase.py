from datetime import datetime

from sqlalchemy import BigInteger, Column
from sqlalchemy.types import DateTime
from sqlmodel import Field, SQLModel


class CallBase(SQLModel):
    recipient_country_code: int
    recipient_number: int = Field(
        index=True, sa_column=Column(BigInteger(), nullable=False)
    )
    duration_in_minutes: int
    start_datetime_iso_8601: datetime = Field(
        index=True, sa_column=Column(DateTime(timezone=True))
    )
    end_datetime_iso_8601: datetime = Field(
        index=True, sa_column=Column(DateTime(timezone=True))
    )
