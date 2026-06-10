"""호환 import 경로 — 실제 구현은 `database`(apps/database.py) 단일 소스.

`from fridge.models.database import Base` 등 기존 import 를 유지한다.
"""

from database import (
    DATABASE_URL,
    AsyncSessionLocal,
    Base,
    dispose_engine,
    engine,
    get_db,
)

__all__ = [
    "DATABASE_URL",
    "AsyncSessionLocal",
    "Base",
    "dispose_engine",
    "engine",
    "get_db",
]
