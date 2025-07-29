from pydantic import BaseModel, Field, field_validator

class PKMSpeciesRequest(BaseModel):
    national_dex_number: int = Field(..., ge=1, description="National Pokédex number, must be >= 1")
    evolution_line_id: int = Field(..., ge=1, description="ID of the evolution line this Pokémon belongs to")
    name_es: str = Field(..., min_length=1, description="Pokémon name in Spanish")
    name_jp: str = Field(..., min_length=1, description="Pokémon name in Japanese")
    generation: int = Field(..., ge=1, description="Generation in which the Pokémon was introduced")
    has_gender_differences: bool = Field(..., description="Indicates if the Pokémon has gender differences")
    description: str = Field(..., min_length=1, description="Pokédex description of the Pokémon")

    @field_validator('name_es', 'name_jp', 'description')
    @classmethod
    def lowercase_name(cls, value: str) -> str:
        return value.strip().lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "national_dex_number": 25,
                "evolution_line_id": 1,
                "name_es": "pikachu",
                "name_jp": "ピカチュウ",
                "generation": 1,
                "has_gender_differences": True,
                "description": "un pokémon eléctrico conocido por sus mejillas que almacenan energía."
            }
        }
    }

class PKMSpeciesResponse(BaseModel):
    id: int
    national_dex_number: int
    evolution_line_id: int
    name_es: str
    name_jp: str
    generation: int
    has_gender_differences: bool
    description: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "national_dex_number": 25,
                "evolution_line_id": 1,
                "name_es": "pikachu",
                "name_jp": "ピカチュウ",
                "generation": 1,
                "has_gender_differences": True,
                "description": "un pokémon eléctrico conocido por sus mejillas que almacenan energía."
            }
        }
    }

