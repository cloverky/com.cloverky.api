from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from fridge.services.ingredient_logic import STORAGE_CHOICES, UNIT_CHOICES


class IngredientItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    quantity: int
    unit: str
    quantity_label: str
    expiry_date: date | None
    purchased_date: date | None = None
    expiry_is_estimated: bool = False
    shelf_life_days: int | None = None
    storage: str
    min_quantity: int
    status: str


class IngredientStatsResponse(BaseModel):
    total: int
    expiring_soon: int
    low_stock: int


class IngredientListResponse(BaseModel):
    items: list[IngredientItemResponse]
    stats: IngredientStatsResponse


class IngredientItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., ge=1, description="개수(정수)")
    unit: str = Field(default="개", max_length=20)
    expiry_date: date | None = None
    purchased_date: date | None = None
    storage: str = Field(default="냉장")
    min_quantity: int = Field(default=1.0, ge=0)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v: str) -> str:
        u = v.strip()
        if u not in UNIT_CHOICES:
            raise ValueError(f"단위는 {', '.join(UNIT_CHOICES)} 중 하나여야 합니다.")
        return u

    @field_validator("storage")
    @classmethod
    def validate_storage(cls, v: str) -> str:
        s = v.strip()
        if s not in STORAGE_CHOICES:
            raise ValueError(f"보관은 {', '.join(STORAGE_CHOICES)} 중 하나여야 합니다.")
        return s


class IngredientItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    quantity: int | None = Field(default=None, ge=1)
    unit: str | None = Field(default=None, max_length=20)
    expiry_date: date | None = None
    storage: str | None = None
    min_quantity: int | None = Field(default=None, ge=0)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str | None) -> str | None:
        return v.strip() if v is not None else None

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v: str | None) -> str | None:
        if v is None:
            return None
        u = v.strip()
        if u not in UNIT_CHOICES:
            raise ValueError(f"단위는 {', '.join(UNIT_CHOICES)} 중 하나여야 합니다.")
        return u

    @field_validator("storage")
    @classmethod
    def validate_storage(cls, v: str | None) -> str | None:
        if v is None:
            return None
        s = v.strip()
        if s not in STORAGE_CHOICES:
            raise ValueError(f"보관은 {', '.join(STORAGE_CHOICES)} 중 하나여야 합니다.")
        return s


class IngredientExpiryEstimateResponse(BaseModel):
    name: str
    purchased_date: date
    storage: str
    shelf_life_days: int
    estimated_expiry_date: date
    message: str


class IngredientQuantityAdjustBody(BaseModel):
    amount: int = Field(default=1, ge=1, description="줄이거나 늘릴 개수")


class IngredientAdjustResponse(BaseModel):
    item: IngredientItemResponse | None = None
    removed: bool = False
    message: str
