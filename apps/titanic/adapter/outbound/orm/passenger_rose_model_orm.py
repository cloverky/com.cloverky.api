from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from clover.core.matrix.grid_neo_theone_base import Base


class RoseModelOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str | None] = mapped_column(String, ForeignKey("passengers.paid"), nullable=True)
    pclass: Mapped[str | None] = mapped_column(String, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String, nullable=True)
    fare: Mapped[str | None] = mapped_column(String, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String, nullable=True)
    embarked: Mapped[str | None] = mapped_column(String, nullable=True)


BookingOrm = RoseModelOrm