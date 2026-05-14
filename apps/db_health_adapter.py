"""DB 연결 확인: 포트(Protocol) + SQLAlchemy 비동기 어댑터."""

from typing import Protocol

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DbHealthPort(Protocol):
    async def check(self) -> dict: ...


class SqlAlchemyAsyncDbHealthAdapter:
    """세션 팩토리로 `SELECT NOW()`를 실행하고 결과를 표준 dict로 반환한다."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | None,
        not_configured_message: str,
    ) -> None:
        self._session_factory = session_factory
        self._not_configured_message = not_configured_message

    async def check(self) -> dict:
        if self._session_factory is None:
            return {"status": "error", "message": self._not_configured_message}
        try:
            async with self._session_factory() as session:
                result = await session.execute(text("SELECT NOW();"))
                now = result.scalar()
            neon = str(now) if now is not None else None
            return {"status": "success", "neon_time": neon}
        except Exception as e:
            return {"status": "error", "message": str(e)}
