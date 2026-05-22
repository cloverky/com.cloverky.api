from pydantic import BaseModel, ConfigDict, Field


class FridgeUserCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    default_storage: str = Field(default="냉장", max_length=20)


class FridgeUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    default_storage: str
