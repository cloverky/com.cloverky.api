from pydantic import BaseModel, Field


class PiperDunnCooSchema(BaseModel):

    id: int = Field(0, description="Character ID")
    name: str = Field("재러드 던", description="Character's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Jared Dunn",
            }
        }
    }

DunnCooSchema = PiperDunnCooSchema
