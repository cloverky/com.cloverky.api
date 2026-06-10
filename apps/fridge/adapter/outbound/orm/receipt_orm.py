from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from models.entity_id import EntityIdMixin


class ReceiptOrm(EntityIdMixin, Base):
    __tablename__ = "receipts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    store_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    purchased_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default="parsed",
        server_default="parsed",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class ReceiptLineOrm(EntityIdMixin, Base):
    __tablename__ = "receipt_lines"

    receipt_id: Mapped[int] = mapped_column(
        ForeignKey("receipts.id", ondelete="CASCADE"),
        index=True,
    )
    line_name: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    unit: Mapped[str] = mapped_column(String(20), default="개", server_default="개")
    food_id: Mapped[int | None] = mapped_column(
        ForeignKey("foods.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    inventory_id: Mapped[int | None] = mapped_column(
        ForeignKey("inventory.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)


FridgeReceipt = ReceiptOrm
FridgeReceiptLine = ReceiptLineOrm
