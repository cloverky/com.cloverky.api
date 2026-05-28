import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.app.ports.input.walter_use_case import WalterUseCase

logger = logging.getLogger(__name__)

walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])
walter_use_case = WalterUseCase()


@walter_router.get("/passengers")
async def list_titanic_passengers(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    result = await walter_use_case.execute(db, page=page, size=size)
    logger.info(
        "[Walter] 승객 목록 조회 — page=%d size=%d returned=%d total=%s",
        page,
        size,
        len(result.get("items", [])),
        (result.get("pagination") or {}).get("totalCount"),
    )
    return result
