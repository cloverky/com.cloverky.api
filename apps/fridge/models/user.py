"""Fridge 전용 회원 확장 — user_controller (기본 users.id 참조)."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fridge.models.database import Base
from models.entity_id import EntityIdMixin


class FridgeUser(EntityIdMixin, Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    default_storage: Mapped[str] = mapped_column(
        String(20),
        default="냉장",
        server_default="냉장",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
