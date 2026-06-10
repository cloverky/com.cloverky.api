from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.receipt_dto import ReceiptParseResultDto


class ReceiptParserPort(ABC):

    @abstractmethod
    def parse(self, image_bytes: bytes, mime_type: str) -> ReceiptParseResultDto:
        pass
