"""Neon DB — Titanic 승객 CSV row ORM."""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from models.entity_id import EntityIdMixin


class TitanicPassengerModel(EntityIdMixin, Base):
    __tablename__ = "titanic_passengers"

    passenger_id: Mapped[int] = mapped_column(Integer, index=True)
    survived: Mapped[int] = mapped_column(Integer)
    pclass: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(255))
    gender: Mapped[str] = mapped_column(String(10))
    age: Mapped[float | None] = mapped_column(Float, nullable=True)
    sibsp: Mapped[int] = mapped_column(Integer)
    parch: Mapped[int] = mapped_column(Integer)
    ticket: Mapped[str] = mapped_column(String(100))
    fare: Mapped[float] = mapped_column(Float)
    cabin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    embarked: Mapped[str | None] = mapped_column(String(5), nullable=True)
