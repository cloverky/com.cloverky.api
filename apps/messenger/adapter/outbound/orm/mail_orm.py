from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from clover.core.matrix.grid_neo_theone_base import Base

_EMBEDDING_DIM = 768


class MailInboxOrm(Base):
    __tablename__ = "mail_inbox"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    from_email: Mapped[str] = mapped_column(String(320))
    subject: Mapped[str | None] = mapped_column(String(998), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    received_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(_EMBEDDING_DIM), nullable=True
    )
