"""
SQLAlchemy 2.0 모던 스타일 — Neon Postgres 비동기 접속 모듈.

- FastAPI 에서는 `engine`, `AsyncSessionLocal`, `get_db`, `Base`, `dispose_engine` 을
  import 해서 사용합니다.
- `python database.py` 로 직접 실행하면 Neon DB 접속 확인 + users 테이블 조회 데모가
  실행됩니다. (작업 디렉터리: `backend/apps`)
"""

from __future__ import annotations

import asyncio
import os
import selectors
import sys
from pathlib import Path

# Windows uvicorn/psycopg async 호환
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from dotenv import load_dotenv
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

# apps/database.py 기준: backend/.env -> apps/.env -> apps/titanic/.env 순으로 로드
_APPS_DIR = Path(__file__).resolve().parent
_BACKEND_ROOT = _APPS_DIR.parent

load_dotenv(_BACKEND_ROOT / ".env")
load_dotenv(_APPS_DIR / ".env")
load_dotenv(_APPS_DIR / "titanic" / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL 이 설정되지 않았습니다. "
        f"{_BACKEND_ROOT / '.env'}, {_APPS_DIR / '.env'}, {_APPS_DIR / 'titanic' / '.env'} "
        "중 한 곳에 DATABASE_URL=... 를 넣어 주세요.",
    )


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10},
    pool_timeout=10,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def dispose_engine() -> None:
    await engine.dispose()


def _mask_dsn(dsn: str) -> str:
    if "@" in dsn:
        head, tail = dsn.split("@", 1)
        if "://" in head and ":" in head.split("://", 1)[1]:
            scheme, rest = head.split("://", 1)
            user, _ = rest.split(":", 1)
            return f"{scheme}://{user}:***@{tail}"
    return dsn


async def main() -> None:
    from models.user import User

    print(f"[Neon] connect to: {_mask_dsn(DATABASE_URL)}")

    async with engine.connect() as conn:
        now = (await conn.execute(text("SELECT NOW()"))).scalar_one()
        version = (await conn.execute(text("SELECT version()"))).scalar_one()
        print(f"[Neon] server time : {now}")
        print(f"[Neon] server ver  : {version}")

    async with AsyncSessionLocal() as session:
        stmt = select(User).order_by(User.id).limit(5)
        result = await session.execute(stmt)
        users = list(result.scalars().all())

        print(f"[Neon] users rows (top 5) : {len(users)}")
        for u in users:
            print(
                f"  - id={u.id} username={u.username!r} "
                f"name={u.name!r} email={u.email!r} role={u.role!r}",
            )

    await dispose_engine()
    print("[Neon] done.")


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main())
        finally:
            loop.close()
    else:
        asyncio.run(main())
