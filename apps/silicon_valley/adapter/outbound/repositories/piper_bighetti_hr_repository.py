from __future__ import annotations

from silicon_valley.app.dtos.piper_bighetti_hr_dto import BighettiHrQuery, BighettiHrResponse
from silicon_valley.app.ports.output.piper_bighetti_hr_port import BighettiHrPort


class BighettiHrPgRepository(BighettiHrPort):

    async def introduce_myself(self, query: BighettiHrQuery) -> BighettiHrResponse:
        return BighettiHrResponse(id=query.id, name=query.name)
