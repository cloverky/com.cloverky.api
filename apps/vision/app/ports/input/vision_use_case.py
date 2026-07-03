from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.vision_dto import VisionQuery, VisionResponse


class VisionUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: VisionQuery) -> VisionResponse:
        pass

    @abstractmethod
    async def upload_image(self, filename: str, content: bytes, content_type: str) -> str:
        """S3에 이미지를 업로드하고 object key를 반환한다."""
        pass
