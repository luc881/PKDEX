from typing import Optional
from pydantic import BaseModel, Field, field_validator

class PKMFormRequest(BaseModel):
    species_id: int = Field(..., gt=0)
    type1_id: int = Field(..., gt=0)
    type2_id: Optional[int] = Field(None, gt=0)
    region_id: int = Field(..., gt=0)
    can_gigantamax: bool = Field(...)
    can_mega: bool = Field(...)
    is_default: bool = Field(...)

    @field_validator("type2_id")
    def validate_type2(cls, v, values):
        if v is not None and v == values.get("type1_id"):
            raise ValueError("type2_id no puede ser igual a type1_id")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "species_id": 1,
                "type1_id": 1,
                "type2_id": 2,
                "region_id": 1,
                "can_gigantamax": True,
                "can_mega": True,
                "is_default": True
            }
        }
    }


class PKMFormResponse(BaseModel):
    id: int
    species_id: int
    type1_id: int
    type2_id: Optional[int]
    region_id: int
    can_gigantamax: bool
    can_mega: bool
    is_default: bool

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "species_id": 1,
                "type1_id": 1,
                "type2_id": 2,
                "region_id": 1,
                "can_gigantamax": True,
                "can_mega": True,
                "is_default": True
            }
        }
    }
