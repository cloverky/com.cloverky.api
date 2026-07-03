from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.ports.output.vision_port import VisionPort


class VisionPgRepository(VisionPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query):
        pass
