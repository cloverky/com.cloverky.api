from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooQuery, DunnCooResponse
from silicon_valley.app.ports.output.piper_dunn_coo_port import DunnCooPort


class DunnCooPgRepository(DunnCooPort):

    def __init__(self, session=None) -> None:
        self.session = session

    async def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        logger.info(f"[DunnCooPgRepository] introduce_myself | {query}")
        return DunnCooResponse(id=query.id, name=query.name)
