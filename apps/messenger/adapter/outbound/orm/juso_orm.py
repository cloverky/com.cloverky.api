"""
인프라 레이어 — ORM ↔ Domain Entity 변환 (Anti-Corruption Layer)
도메인 객체가 SQLAlchemy를 직접 의존하지 않도록 매핑 책임을 여기서 담당.
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from clover.core.matrix.grid_neo_theone_base import Base


# ──────────────────────────────────────────────
# ORM Model (인프라 관심사만 담당)
# ──────────────────────────────────────────────
class ContactOrm(Base):
    """Google Contacts CSV 한 행에 대응하는 테이블.

    CSV 헤더:
    First Name, Middle Name, Last Name,
    Phonetic First Name, Phonetic Middle Name, Phonetic Last Name,
    Name Prefix, Name Suffix, Nickname, File As,
    Organization Name, Organization Title, Organization Department,
    Birthday, Notes, Photo, Labels,
    E-mail 1 - Label, E-mail 1 - Value,
    Phone 1 - Label, Phone 1 - Value
    """

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 이름
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    name_prefix: Mapped[str | None] = mapped_column(String, nullable=True)
    name_suffix: Mapped[str | None] = mapped_column(String, nullable=True)
    nickname: Mapped[str | None] = mapped_column(String, nullable=True)
    file_as: Mapped[str | None] = mapped_column(String, nullable=True)

    # 조직
    organization_name: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_title: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_department: Mapped[str | None] = mapped_column(String, nullable=True)

    # 기타
    birthday: Mapped[str | None] = mapped_column(String, nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    photo: Mapped[str | None] = mapped_column(String, nullable=True)
    labels: Mapped[str | None] = mapped_column(String, nullable=True)

    # 이메일
    email_1_label: Mapped[str | None] = mapped_column(String, nullable=True)
    email_1_value: Mapped[str | None] = mapped_column(String, nullable=True)

    # 전화
    phone_1_label: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_1_value: Mapped[str | None] = mapped_column(String, nullable=True)


# ──────────────────────────────────────────────
# Mapper alias
# ──────────────────────────────────────────────
PersonOrm = ContactOrm
