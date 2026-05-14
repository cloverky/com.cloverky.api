import logging
import os
from collections.abc import AsyncGenerator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)

DB_UNAVAILABLE_DETAIL = (
    "DATABASE_URL이 설정되지 않았거나 엔진 초기화에 실패했습니다. 저장소 루트의 .env를 확인하세요."
)

# database.py 위치: .../backend/apps/ → 저장소 루트는 parents[4]
_REPO_ROOT = Path(__file__).resolve().parents[4]
load_dotenv(_REPO_ROOT / ".env")
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


def _normalize_database_url(raw_url: str) -> str:
    # psycopg2 기본 해석을 피하고, requirements에 있는 psycopg 드라이버를 사용한다.
    if raw_url.startswith("postgres://"):
        return "postgresql+psycopg://" + raw_url[len("postgres://") :]
    if raw_url.startswith("postgresql://") and "+psycopg" not in raw_url:
        return "postgresql+psycopg://" + raw_url[len("postgresql://") :]
    return raw_url

if not DATABASE_URL:
    logger.warning(
        "DATABASE_URL이 없습니다. /db-check는 오류 JSON을 반환하고, "
        "get_db를 쓰는 다른 엔드포인트는 503을 반환합니다. "
        "설정: %s",
        _REPO_ROOT / ".env",
    )
else:
    try:
        normalized_database_url = _normalize_database_url(DATABASE_URL)
        if normalized_database_url != DATABASE_URL:
            logger.info("DATABASE_URL 드라이버를 psycopg로 보정했습니다.")
        engine = create_async_engine(normalized_database_url, echo=True)
        AsyncSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    except Exception:
        logger.exception("비동기 DB 엔진 생성에 실패했습니다.")
        engine = None
        AsyncSessionLocal = None

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    from fastapi import HTTPException

    if AsyncSessionLocal is None:
        raise HTTPException(status_code=503, detail=DB_UNAVAILABLE_DETAIL)
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.exception("DB 세션 처리 중 오류가 발생했습니다.")
            raise
