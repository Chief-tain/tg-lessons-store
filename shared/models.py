from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    SmallInteger,
    String,
    Table,
    UniqueConstraint,
    LargeBinary,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, FLOAT, INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class"""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        "id", BigInteger, primary_key=True, autoincrement=False
    )
    username: Mapped[str] = mapped_column("username", String, nullable=True)
    first_name: Mapped[str] = mapped_column("first_name", String)
    last_name: Mapped[str] = mapped_column("last_name", String, nullable=True)
    language_code: Mapped[str] = mapped_column("language_code", String(2))
    registered_at: Mapped[datetime] = mapped_column(
        "registered_at", DateTime, server_default=func.now(), nullable=False
    )
    bought_lessons_id: Mapped[list[INTEGER]] = mapped_column(
        "bought_lessons_id", ARRAY(INTEGER), nullable=True, default=[]
    )


class Lessons(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    language: Mapped[str] = mapped_column("language", String, nullable=True)
    name: Mapped[str] = mapped_column("name", String, nullable=True)
    description: Mapped[str] = mapped_column("description", String, nullable=True)
    voice_urls: Mapped[list[str]] = mapped_column(
        "voice_urls", ARRAY(String), nullable=True, default=[]
    )
    doc_urls: Mapped[list[str]] = mapped_column(
        "doc_urls", ARRAY(String), nullable=True, default=[]
    )
    price: Mapped[float] = mapped_column("price", FLOAT, nullable=True, default=None)
    is_available: Mapped[bool] = mapped_column(
        "is_available", Boolean, nullable=True, default=True
    )


class Payments(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        "user_id", BigInteger, nullable=False, default=None
    )
    lesson_id: Mapped[int] = mapped_column(
        "lesson_id", Integer, nullable=False, default=None
    )
    price: Mapped[float] = mapped_column("price", FLOAT, nullable=True, default=None)
    payment_at: Mapped[datetime] = mapped_column(
        "payment_at", DateTime, server_default=func.now(), nullable=False
    )
