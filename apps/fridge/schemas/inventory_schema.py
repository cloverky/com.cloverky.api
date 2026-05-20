from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class InventoryCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    food_id: int = Field(..., ge=1)
    quantity: int = Field(default=1, ge=1)
    unit: str = Field(default="개", max_length=20)
    expiry_date: date | None = None
    purchased_date: date | None = None
    expiry_is_estimated: bool = False
    storage: str = Field(default="냉장", max_length=20)


class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    food_id: int
    quantity: int
    unit: str
    expiry_date: date | None
    purchased_date: date | None
    expiry_is_estimated: bool
    storage: str
