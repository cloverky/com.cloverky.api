"""
Alembic migration environment — Neon Postgres (sync psycopg driver).

DATABASE_URL 은 backend/.env 에서 읽습니다.
Alembic 은 동기 엔진이 필요하므로 postgresql+psycopg:// 로 변환합니다.
"""

from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

# backend/alembic/env.py -> backend/
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_APPS_DIR = _BACKEND_ROOT / "apps"

sys.path.insert(0, str(_APPS_DIR))

load_dotenv(_BACKEND_ROOT / ".env")
load_dotenv(_APPS_DIR / ".env")

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _get_sync_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL 이 설정되지 않았습니다. "
            f"{_BACKEND_ROOT / '.env'} 에 Neon 연결 문자열을 넣어 주세요.",
        )
    # Alembic 은 동기 드라이버 사용 (앱은 psycopg_async 가능)
    return (
        url.replace("postgresql+psycopg_async://", "postgresql+psycopg://")
        .replace("postgresql+asyncpg://", "postgresql+psycopg://")
    )


# 모델 메타데이터 — autogenerate 용
from fridge.models.database import Base  # noqa: E402
from models.user import User  # noqa: E402, F401

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", _get_sync_database_url())


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
