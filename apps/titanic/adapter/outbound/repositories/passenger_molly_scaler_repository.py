from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_molly_scaler_dto import (
    MollyScalerQuery,
    MollyScalerResponse,
)
from titanic.app.ports.output.passenger_molly_scaler_port import MollyScalerPort


class MollyScalerPgRepository(MollyScalerPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: MollyScalerQuery) -> MollyScalerResponse:
        """몰리 스케일러의 자기 소개 레포지토리 구현 메소드"""

        logger.info(
            f"[MollyScalerPgRepository] introduce_myself 진입 | request_data={query}"
        )

        response: MollyScalerResponse = MollyScalerResponse(
            id=query.id * 10000, name=query.name + "가 레포지토리에 다녀옴"
        )
        return response
