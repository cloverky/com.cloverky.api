from pydantic import BaseModel, ConfigDict, Field


class CodeCreate(BaseModel):
    food_id: int = Field(..., ge=1)
    code: str = Field(..., min_length=1, max_length=64)
    code_type: str = Field(default="barcode", max_length=32)


class CodeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    food_id: int
    code: str
    code_type: str
