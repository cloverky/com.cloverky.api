from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from fridge.app.dtos.receipt_dto import ReceiptLineDto


class ReceiptRepository(ABC):

    @abstractmethod
    async def create_receipt(
        self,
        user_id: int,
        store_name: str | None,
        purchased_date: date | None,
        status: str,
    ) -> int:
        pass

    @abstractmethod
    async def create_line(
        self,
        receipt_id: int,
        line_name: str,
        quantity: int,
        unit: str,
        food_id: int | None,
        inventory_id: int | None,
    ) -> ReceiptLineDto:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
