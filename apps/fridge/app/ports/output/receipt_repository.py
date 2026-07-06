from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.receipt_dto import ReceiptQuery, ReceiptUploadResponse


class ReceiptRepository(ABC):
    @abstractmethod
    async def get_status(self, query: ReceiptQuery) -> ReceiptUploadResponse:
        pass
