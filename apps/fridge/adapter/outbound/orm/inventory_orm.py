from __future__ import annotations

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class InventoryOrm(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[str | None] = mapped_column(String, nullable=True)
    expiry_date: Mapped[str | None] = mapped_column(Date, nullable=True)
    purchased_date: Mapped[str | None] = mapped_column(Date, nullable=True)
    expiry_is_estimated: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    storage: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    food_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("foods.id"), nullable=True
    )
