import os
from typing import Generator

from sqlmodel import Session, create_engine

DATABASE_URL = os.environ.get("DATABASE_URL", "")


def get_session() -> Generator:
    engine = create_engine(DATABASE_URL, echo=True)
    with Session(engine) as session:
        yield session
