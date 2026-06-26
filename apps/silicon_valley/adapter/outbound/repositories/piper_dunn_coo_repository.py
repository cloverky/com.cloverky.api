from __future__ import annotations

from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooQuery, DunnCooResponse
from silicon_valley.app.ports.output.piper_dunn_coo_port import DunnCooPort


class DunnCooPgRepository(DunnCooPort):

    async def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        return DunnCooResponse(id=query.id, name=query.name)
