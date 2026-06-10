from __future__ import annotations

from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from clover.core.matrix.grid_neo_theone_base import Base


class JackTrainerOrm(Base):
    __tablename__ = "passengers"
    __table_args__ = (UniqueConstraint("passenger_id", name="uq_passengers_passenger_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str | None] = mapped_column(String, nullable=True, unique=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(String, nullable=True)
    sib_sp: Mapped[str | None] = mapped_column(String, nullable=True)
    parch: Mapped[str | None] = mapped_column(String, nullable=True)
    survived: Mapped[str | None] = mapped_column(String, nullable=True)


PersonOrm = JackTrainerOrm
