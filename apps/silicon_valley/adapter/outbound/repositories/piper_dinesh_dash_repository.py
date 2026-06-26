from __future__ import annotations

from silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashQuery, DineshDashResponse
from silicon_valley.app.ports.output.piper_dinesh_dash_port import DineshDashPort


class DineshDashPgRepository(DineshDashPort):

    async def introduce_myself(self, query: DineshDashQuery) -> DineshDashResponse:
        return DineshDashResponse(id=query.id, name=query.name)
