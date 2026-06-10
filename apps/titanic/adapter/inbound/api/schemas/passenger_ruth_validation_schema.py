from pydantic import BaseModel, Field

class RuthValidationSchema(BaseModel):
    
    id: int = Field(0, description="Passenger ID")
    name: str = Field("루쓰 드윗 부카터", description="Passenger's name")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 12,
                "name": "Ruth DeWitt Bukater"
            }
        }
    }