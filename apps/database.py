"""호환 레이어 — 구현은 core/database.py."""

from core.database import (
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
