from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fridge.models.database import Base
from models.entity_id import EntityIdMixin


class IngredientManager(EntityIdMixin, Base):
    """회원별 나만의냉장고 식재료 — Ingredient Manager가 관리하는 행."""

    __tablename__ = "ingredient_manager"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit: Mapped[str] = mapped_column(String(20), default="개")
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    purchased_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_is_estimated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    storage: Mapped[str] = mapped_column(String(20), default="냉장")
    min_quantity: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
