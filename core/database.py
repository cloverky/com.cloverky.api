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

# 1. 경로 설정 및 환경 변수 로드
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_APPS_DIR = _BACKEND_ROOT / "apps"

load_dotenv(_BACKEND_ROOT / ".env")
load_dotenv(_APPS_DIR / ".env")
load_dotenv(_APPS_DIR / "titanic" / ".env")


# 2. Neon 데이터베이스 URL 스키마 보정 함수
def _resolve_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL 이 설정되지 않았습니다. "
            f"{_BACKEND_ROOT / '.env'} 에 Neon 연결 문자열을 넣어 주세요.",
        )
        
    # SQLAlchemy 2.0 + psycopg(v3) 비동기 드라이버 규격 적용
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg_async://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg_async://", 1)
    return url


DATABASE_URL = _resolve_database_url()


# 3. SQLAlchemy 2.0 스타일 Declarative Base 선언
class Base(DeclarativeBase):
    """모든 DB 모델이 상속받을 최신 스타일의 Base 클래스"""
    pass


# 4. 비동기 엔진 생성 (클라우드 환경 최적화 옵션 추가)
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # 💡 Neon 클라우드 연결이 끊겼는지 미리 체크 후 재연결 (필수)
    pool_size=5,         # 기본 유지할 커넥션 개수
    max_overflow=10,     # 트래픽 몰릴 때 추가 허용할 커넥션 개수
)

# 5. 최신 2.0 전용 비동기 세션 팩토리 생성
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 커밋 후 지연 로딩 에러 방지
)


# 6. 의존성 주입(DI)을 위한 비동기 세션 제너레이터
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 등에서 세션을 주입받아 사용하기 위한 안전한 비동기 컨텍스트"""
    async with AsyncSessionLocal() as session:
        yield session


# 7. 애플리케이션 종료 시 안전한 엔진 해제 함수
async def dispose_engine() -> None:
    """애플리케이션 셧다운 시 커넥션 풀을 안전하게 닫아줍니다."""
    await engine.dispose()