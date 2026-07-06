from __future__ import annotations

from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import (
    GilfoyleSysQuery,
    GilfoyleSysResponse,
)
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import GilfoyleSysPort


class GilfoyleSysPgRepository(GilfoyleSysPort):
    async def introduce_myself(self, query: GilfoyleSysQuery) -> GilfoyleSysResponse:
        return GilfoyleSysResponse(id=query.id, name=query.name)
