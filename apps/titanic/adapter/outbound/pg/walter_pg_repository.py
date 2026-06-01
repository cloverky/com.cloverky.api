from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.titanic_passenger_model import TitanicPassengerModel
from titanic.app.ports.output.walter_repository import WalterRepository

logger = logging.getLogger(__name__)


class WalterPgRepository(WalterRepository):
    """WalterRepository 출력 포트 — Neon 승객 목록 조회 어댑터."""

    async def list_passengers(
        self,
        db: AsyncSession,
        *,
        page: int,
        size: int,
    ) -> dict[str, Any]:
        total_result = await db.execute(
            select(func.count(func.distinct(TitanicPassengerModel.passenger_id))),
        )
        total_count = int(total_result.scalar_one() or 0)
        offset = (page - 1) * size

        latest_ids = (
            select(func.max(TitanicPassengerModel.id).label("id"))
            .group_by(TitanicPassengerModel.passenger_id)
            .subquery()
        )

        result = await db.execute(
            select(TitanicPassengerModel)
            .join(latest_ids, TitanicPassengerModel.id == latest_ids.c.id)
            .order_by(TitanicPassengerModel.passenger_id.asc())
            .offset(offset)
            .limit(size)
        )
        rows = list(result.scalars().all())
        total_pages = (total_count + size - 1) // size if total_count > 0 else 1

        passengers = [
            {
                "id": row.id,
                "passengerId": row.passenger_id,
                "name": row.name,
                "gender": row.gender,
                "age": row.age,
                "pclass": row.pclass,
                "survived": row.survived,
                "ticket": row.ticket,
                "fare": row.fare,
                "embarked": row.embarked,
            }
            for row in rows
        ]

        logger.info(
            "🎈 [WalterPg] 승객 목록 조회 완료 — page=%d size=%d returned=%d total=%d",
            page,
            size,
            len(passengers),
            total_count,
        )

        return {
            "items": passengers,
            "pagination": {
                "page": page,
                "size": size,
                "totalCount": total_count,
                "totalPages": total_pages,
            },
        }
