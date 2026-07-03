from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.vision_dto import VisionQuery, VisionResponse


class VisionPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: VisionQuery) -> VisionResponse:
        pass
