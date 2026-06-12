"""
인프라 레이어 — ORM ↔ Domain Entity 변환 (Anti-Corruption Layer)
도메인 객체가 SQLAlchemy를 직접 의존하지 않도록 매핑 책임을 여기서 담당.
"""
from __future__ import annotations
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# ──────────────────────────────────────────────
# ORM Model (인프라 관심사만 담당)
# ──────────────────────────────────────────────
class JackTrainerOrm(Base):
    __tablename__ = "passengers"

    passenger_id: Mapped[str | None] = mapped_column(String, primary_key=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(String, nullable=True)
    sib_sp: Mapped[str | None] = mapped_column(String, nullable=True)
    parch: Mapped[str | None] = mapped_column(String, nullable=True)
    survived: Mapped[str | None] = mapped_column(String, nullable=True)


# ──────────────────────────────────────────────
# Mapper: ORM ↔ Entity 변환
# ──────────────────────────────────────────────
PersonOrm = JackTrainerOrm