from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

from silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashQuery, DineshDashResponse
from silicon_valley.app.ports.output.piper_dinesh_dash_port import DineshDashPort


class DineshDashPgRepository(DineshDashPort):

    def __init__(self, session=None) -> None:
        self.session = session

    async def introduce_myself(self, query: DineshDashQuery) -> DineshDashResponse:
        logger.info(f"[DineshDashPgRepository] introduce_myself | {query}")
        return DineshDashResponse(id=query.id, name=query.name)
