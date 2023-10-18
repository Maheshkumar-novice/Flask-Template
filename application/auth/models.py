from typing import Optional

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from database.resource import Base, DefaultTimeStamps
from flask_login import UserMixin

class User(Base, DefaultTimeStamps, UserMixin):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('email', name='unique_user_emails'),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[Optional[str]] = mapped_column(String(300))
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(200))
    is_google_user: Mapped[bool] = mapped_column(
        default=False, server_default=expression.false())
    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=expression.true())
    is_deleted: Mapped[bool] = mapped_column(
        default=False, server_default=expression.false())
