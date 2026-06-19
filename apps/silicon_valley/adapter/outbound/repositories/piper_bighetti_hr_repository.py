from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

from silicon_valley.app.dtos.piper_bighetti_hr_dto import BighettiHrQuery, BighettiHrResponse
from silicon_valley.app.ports.output.piper_bighetti_hr_port import BighettiHrPort


class BighettiHrPgRepository(BighettiHrPort):

    def __init__(self, session=None) -> None:
        self.session = session

    async def introduce_myself(self, query: BighettiHrQuery) -> BighettiHrResponse:
        logger.info(f"[BighettiHrPgRepository] introduce_myself | {query}")
        return BighettiHrResponse(id=query.id, name=query.name)
