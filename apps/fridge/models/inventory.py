"""회원별 냉장고 재고(식품 단위) — inventory_controller."""

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fridge.models.database import Base
from models.entity_id import EntityIdMixin


class FridgeInventory(EntityIdMixin, Base):
    __tablename__ = "inventory"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    food_id: Mapped[int] = mapped_column(
        ForeignKey("foods.id", ondelete="CASCADE"),
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    unit: Mapped[str] = mapped_column(String(20), default="개", server_default="개")
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    purchased_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_is_estimated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    storage: Mapped[str] = mapped_column(String(20), default="냉장", server_default="냉장")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
