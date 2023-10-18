import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    scoped_session,
    sessionmaker,
)
from typing_extensions import Annotated

from config import Config

DBSession = scoped_session(
    sessionmaker(bind=create_engine(Config.DB_URL, echo=True)))


class Base(DeclarativeBase):
    pass


class DefaultTimeStamps:
    _timestamp = Annotated[
        datetime.datetime,
        mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
    ]
    created_at: Mapped[_timestamp]
    updated_at: Mapped[_timestamp]


__all__ = ['Session', 'Base', 'DefaultTimeStamps']
