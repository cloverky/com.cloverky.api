from dataclasses import dataclass
from datetime import date


@dataclass
class ReceiptLineParsedDto:
    name: str
    quantity: int
    unit: str


@dataclass
class ReceiptParseResultDto:
    store_name: str | None
    purchased_date: date | None
    items: list[ReceiptLineParsedDto]


@dataclass
class ReceiptLineDto:
    id: int
    line_name: str
    quantity: int
    unit: str
    food_id: int | None
    inventory_id: int | None


@dataclass
class ReceiptScanResultDto:
    receipt_id: int
    store_name: str | None
    purchased_date: date | None
    status: str
    lines: list[ReceiptLineDto]
    inventory_created: int
