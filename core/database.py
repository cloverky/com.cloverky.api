"""Neon Postgres 연결 — SQLAlchemy async 엔진·세션 (인프라 레이어)."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_APPS_DIR = _BACKEND_ROOT / "apps"

load_dotenv(_BACKEND_ROOT / ".env")
load_dotenv(_APPS_DIR / ".env")
load_dotenv(_APPS_DIR / "titanic" / ".env")


def _resolve_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL 이 설정되지 않았습니다. "
            f"{_BACKEND_ROOT / '.env'} 에 Neon 연결 문자열을 넣어 주세요.",
        )
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg_async://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg_async://", 1)
    return url


DATABASE_URL = _resolve_database_url()


class Base(DeclarativeBase):
    pass


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def dispose_engine() -> None:
    await engine.dispose()
