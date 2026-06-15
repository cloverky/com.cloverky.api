from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.adapter.inbound.api.schemas.receipt_line_schema import ReceiptLineSchema
from clover.apps.fridge.app.dtos.receipt_line_dto import ReceiptLineResponse


class ReceiptLineUseCase(ABC):

    @abstractmethod
    async def get_lines(self, schema: ReceiptLineSchema) -> ReceiptLineResponse:
        pass
