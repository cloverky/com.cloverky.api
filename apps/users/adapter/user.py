import enum
from datetime import datetime

from database import Base
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from users.adapter.entity_id import EntityIdMixin


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(EntityIdMixin, Base):
    """FridgeAI 회원 — 비밀번호·역할 포함."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        String(20),
        default=UserRole.USER.value,
        server_default=UserRole.USER.value,
    )
    agree_terms: Mapped[bool] = mapped_column(Boolean, default=True)
    default_storage: Mapped[str] = mapped_column(
        String(20),
        default="냉장",
        server_default="냉장",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
