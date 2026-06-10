from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ReceiptLineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    line_name: str
    quantity: int
    unit: str
    food_id: int | None
    inventory_id: int | None


class ReceiptScanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    receipt_id: int
    store_name: str | None
    purchased_date: date | None
    status: str
    lines: list[ReceiptLineResponse]
    inventory_created: int
