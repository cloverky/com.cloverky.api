from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.receipt_line_dto import ReceiptLineResponse
from fridge.adapter.inbound.api.schemas.receipt_line_schema import ReceiptLineSchema


class ReceiptLineUseCase(ABC):
    @abstractmethod
    async def get_lines(self, schema: ReceiptLineSchema) -> ReceiptLineResponse:
        pass
