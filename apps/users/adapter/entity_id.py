"""공통 PK — docs/DevOps/Backend/ENTITY_RULE.md"""

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class EntityIdMixin:
    """시스템 내부용 자동 증감 고유 번호 (기본 키). 컬럼명은 항상 `id`."""

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
