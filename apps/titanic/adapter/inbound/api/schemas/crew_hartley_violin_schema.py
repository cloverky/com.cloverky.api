from pydantic import BaseModel, Field

class HartleyViolinSchema(BaseModel):
    
    id: int = Field(0, description="Violin ID")
    name: str = Field("월리스 하틀리", description="Violinist's name")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Wallace Hartley",
            }
        }
    }