"""
인프라 레이어 — ORM ↔ Domain Entity 변환 (Anti-Corruption Layer)
도메인 객체가 SQLAlchemy를 직접 의존하지 않도록 매핑 책임을 여기서 담당.
"""
from __future__ import annotations
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from clover.apps.titanic.domain.entities import Passenger
from clover.apps.titanic.domain.value_objects import (
    PassengerId, PassengerName, Gender, Age, FamilyInfo, SurvivalStatus,
)


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
class PassengerMapper:

    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> Passenger:
        """ORM row → Domain Entity"""
        return Passenger.create(
            db_id=orm.id,
            passenger_id=orm.passenger_id or "",
            name=orm.name or "",
            gender=orm.gender or "",
            age=float(orm.age) if orm.age is not None else None,
            sib_sp=int(orm.sib_sp) if orm.sib_sp is not None else 0,
            parch=int(orm.parch) if orm.parch is not None else 0,
            survived=orm.survived,
        )

    @staticmethod
    def to_orm(entity: Passenger, existing: Optional[JackTrainerOrm] = None) -> JackTrainerOrm:
        """
        Domain Entity → ORM row.
        existing을 넘기면 기존 row를 갱신(UPDATE), 없으면 새 row 생성(INSERT).
        """
        orm = existing or JackTrainerOrm()
        orm.passenger_id = entity.passenger_id.value
        orm.name = entity.name.value
        orm.gender = entity.gender.value
        orm.age = str(entity.age.value) if entity.age else None
        orm.sib_sp = str(entity.family_info.sib_sp)
        orm.parch = str(entity.family_info.parch)
        orm.survived = entity.survival_status.value
        return orm


PersonOrm = JackTrainerOrm