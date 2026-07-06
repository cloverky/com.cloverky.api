from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.receipt_line_dto import (
    ReceiptLineQuery,
    ReceiptLineResponse,
)


class ReceiptLineRepository(ABC):
    @abstractmethod
    async def get_lines(self, query: ReceiptLineQuery) -> ReceiptLineResponse:
        pass
