from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.adapter.inbound.api.schemas.receipt_schema import ReceiptUploadSchema
from clover.apps.fridge.app.dtos.receipt_dto import ReceiptUploadResponse


class ReceiptUseCase(ABC):

    @abstractmethod
    async def get_status(self, schema: ReceiptUploadSchema) -> ReceiptUploadResponse:
        pass
