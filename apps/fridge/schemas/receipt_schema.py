from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ReceiptLineParsed(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(default=1, ge=1)
    unit: str = Field(default="개", max_length=20)


class ReceiptParseResult(BaseModel):
    store_name: str | None = None
    purchased_date: date | None = None
    items: list[ReceiptLineParsed] = Field(default_factory=list)


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
