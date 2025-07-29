from pydantic import BaseModel, Field, field_validator
from typing import Literal

class TypesRequest(BaseModel):
    name: Literal[
        "normal", "fire", "water", "electric", "grass", "ice",
        "fighting", "poison", "ground", "flying", "psychic", "bug",
        "rock", "ghost", "dragon", "dark", "steel", "fairy"
    ] = Field(..., description="Pokemon type")

    @field_validator('name')
    @classmethod
    def lowercase_name(cls, value: str) -> str:
        return value.strip().lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "dark"
            }
        }
    }

class TypesResponse(BaseModel):
    id: int
    name: str


    model_config = {"from_attributes": True}
