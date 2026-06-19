from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoQuery, HendricksCeoResponse
from silicon_valley.app.ports.output.piper_hendricks_ceo_port import HendricksCeoPort


class HendricksCeoPgRepository(HendricksCeoPort):

    def __init__(self, session=None) -> None:
        self.session = session

    async def introduce_myself(self, query: HendricksCeoQuery) -> HendricksCeoResponse:
        logger.info(f"[HendricksCeoPgRepository] introduce_myself | {query}")
        return HendricksCeoResponse(id=query.id, name=query.name)
