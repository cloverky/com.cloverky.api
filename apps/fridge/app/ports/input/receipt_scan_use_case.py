from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.receipt_dto import ReceiptScanResultDto


class ReceiptScanUseCase(ABC):

    @abstractmethod
    async def scan_receipt(
        self,
        user_email: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> ReceiptScanResultDto:
        pass
