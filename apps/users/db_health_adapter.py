from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DbHealthAdapter:
    """Neon 등 비동기 DB 세션으로 헬스 체크."""

    @staticmethod
    async def neon_time_check(db: AsyncSession) -> dict:
        try:
            result = await db.execute(text("SELECT NOW();"))
            now = result.scalar()
            return {
                "status": "success",
                "neon_time": str(now) if now is not None else None,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
