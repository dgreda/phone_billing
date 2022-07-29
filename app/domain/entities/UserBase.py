from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    country_code: int
    number: int = Field(
        index=True, sa_column=Column(BigInteger(), nullable=False)
    )
