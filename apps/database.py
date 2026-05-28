"""호환 레이어 — 구현은 backend/core/database.py."""

import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parent.parent / "core" / "database.py"
_spec = importlib.util.spec_from_file_location("backend_database", _path)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"database 모듈을 로드할 수 없습니다: {_path}")

_backend = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_backend)

DATABASE_URL = _backend.DATABASE_URL
AsyncSessionLocal = _backend.AsyncSessionLocal
Base = _backend.Base
dispose_engine = _backend.dispose_engine
engine = _backend.engine
get_db = _backend.get_db

__all__ = [
    "DATABASE_URL",
    "AsyncSessionLocal",
    "Base",
    "dispose_engine",
    "engine",
    "get_db",
]
