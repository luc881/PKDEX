from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ....models.pokemon_species.orm import PKMSpecies
from ....db.session import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....models.pokemon_species.schemas import PKMSpeciesRequest, PKMSpeciesResponse
# from .auth import get_current_user

router = APIRouter(
    prefix="/pkmspecies",
    tags=["PKMSpecies"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/',
            response_model=list[PKMSpeciesResponse],
            summary="List all Pokémon species",
            description="Retrieve all Pokémon species currently stored in the database.",
            status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    todos = db.query(PKMSpecies).all()
    return todos

@router.post(    '/',
            status_code=status.HTTP_201_CREATED,
            response_model=PKMSpeciesResponse,
            summary="Create a new Pokémon species",
            description="Adds a new Pokémon species to the database.")
async def create_pkmspecies(db: db_dependency, pkmspecies_request: PKMSpeciesRequest):
    pkmspecies_model = PKMSpecies(**pkmspecies_request.model_dump())

    pkmspecies_duplicate = db.query(PKMSpecies).filter(
        (PKMSpecies.national_dex_number == pkmspecies_model.national_dex_number) |
        (PKMSpecies.name_es == pkmspecies_model.name_es) |
        (PKMSpecies.name_jp == pkmspecies_model.name_jp)
    ).first()

    if pkmspecies_duplicate:
        if pkmspecies_duplicate.national_dex_number == pkmspecies_model.national_dex_number:
            field = "national_dex_number"
        elif pkmspecies_duplicate.name_es == pkmspecies_model.name_es:
            field = "name_es"
        else:
            field = "name_jp"

        raise HTTPException(
            status_code=409,
            detail=f"Pokémon species with the same {field} already exists"
        )

    db.add(pkmspecies_model)
    db.commit()
    db.refresh(pkmspecies_model)  # Refresh to get the ID and other generated fields
    return pkmspecies_model


