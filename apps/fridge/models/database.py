"""compat — main.py 레거시 import 유지용. 구현은 core/database.py."""

from database import (
    Base,
    dispose_engine,
    engine,
    get_db,
)

__all__ = ["Base", "dispose_engine", "engine", "get_db"]
