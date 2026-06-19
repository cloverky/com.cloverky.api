from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import GilfoyleSysQuery, GilfoyleSysResponse
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import GilfoyleSysPort


class GilfoyleSysPgRepository(GilfoyleSysPort):

    def __init__(self, session=None) -> None:
        self.session = session

    async def introduce_myself(self, query: GilfoyleSysQuery) -> GilfoyleSysResponse:
        logger.info(f"[GilfoyleSysPgRepository] introduce_myself | {query}")
        return GilfoyleSysResponse(id=query.id, name=query.name)
