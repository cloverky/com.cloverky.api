"""식품 식별 코드(바코드 등) — code_controller."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fridge.models.database import Base
from models.entity_id import EntityIdMixin


class FridgeCode(EntityIdMixin, Base):
    __tablename__ = "codes"

    food_id: Mapped[int] = mapped_column(
        ForeignKey("fridge_foods.id", ondelete="CASCADE"),
        index=True,
    )
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    code_type: Mapped[str] = mapped_column(
        String(32),
        default="barcode",
        server_default="barcode",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
