from pydantic import BaseModel, ConfigDict, Field


class FoodCreate(BaseModel):
    category_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    default_unit: str = Field(default="개", max_length=20)


class FoodRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    description: str | None
    default_unit: str
