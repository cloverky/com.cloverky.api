from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.receipt_dto import ReceiptUploadResponse
from fridge.adapter.inbound.api.schemas.receipt_schema import ReceiptUploadSchema


class ReceiptUseCase(ABC):
    @abstractmethod
    async def get_status(self, schema: ReceiptUploadSchema) -> ReceiptUploadResponse:
        pass
