from dataclasses import dataclass


@dataclass(frozen=True)
class ReceiptLineQuery:
    receipt_id: int


@dataclass(frozen=True)
class ReceiptLineResponse:
    id: int
    line_name: str
