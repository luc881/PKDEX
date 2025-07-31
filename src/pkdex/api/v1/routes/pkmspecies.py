from fastapi import Depends, HTTPException, APIRouter, Path
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

@router.put("/{pkmspecies_id}", status_code=status.HTTP_200_OK,
            response_model=PKMSpeciesResponse,
            summary="Update a Pokémon species",
            description="Updates a Pokémon species to the database."
            )
async def update_pkmspecies(db: db_dependency, pkmspecies_request: PKMSpeciesRequest, pkmspecies_id: int = Path(..., gt=0, description="The ID of the pkm species item to update.")):

    pkmspecies = db.query(PKMSpecies).filter(PKMSpecies.id == pkmspecies_id).first()

    if not pkmspecies:
        raise HTTPException(status_code=404, detail="Pokémon species not found")

    # Validar duplicados para los campos únicos
    duplicate = db.query(PKMSpecies).filter(
        ((PKMSpecies.national_dex_number == pkmspecies_request.national_dex_number) |
        (PKMSpecies.name_es == pkmspecies_request.name_es) |
        (PKMSpecies.name_jp == pkmspecies_request.name_jp)) &
        (PKMSpecies.id != pkmspecies_id)  # Ignorar el registro actual
    ).first()

    if duplicate:
        if duplicate.national_dex_number == pkmspecies_request.national_dex_number:
            field = "national_dex_number"
        elif duplicate.name_es == pkmspecies_request.name_es:
            field = "name_es"
        else:
            field = "name_jp"

        raise HTTPException(
            status_code=409,
            detail=f"Pokémon species with the same {field} already exists"
        )

    for key, value in pkmspecies_request.model_dump().items():
        setattr(pkmspecies, key, value)

    db.commit()

    return pkmspecies

@router.delete("/{pkmspecies_id}", status_code=status.HTTP_200_OK,
            response_model=PKMSpeciesResponse,
            summary="Delete a Pokémon species",
            description="Delete a Pokémon species to the database."
            )
async def delete_pkmspecies(db: db_dependency, pkmspecies_request: PKMSpeciesRequest, pkmspecies_id: int = Path(..., gt=0, description="The ID of the pkm species item to update.")):

    pkmspecies = db.query(PKMSpecies).filter(PKMSpecies.id == pkmspecies_id).first()

    if not pkmspecies:
        raise HTTPException(status_code=404, detail="Pokémon species not found")

    db.delete(pkmspecies)
    db.commit()

    return pkmspecies
