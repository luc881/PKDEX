from pydantic import BaseModel, Field, field_validator
from typing import Literal

class RegionsRequest(BaseModel):
    name: Literal[
        'kanto', 'johto', 'hoenn', 'sinnoh', 'hisui', 'unova', 'kalos', 'alola', 'galar', 'paldea'
    ] = Field(..., description="Pokemon region")

    @field_validator('name')
    @classmethod
    def lowercase_name(cls, value: str) -> str:
        return value.strip().lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "paldea"
            }
        }
    }

class RegionsResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
