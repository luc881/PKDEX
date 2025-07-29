from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ....models.types.orm import Types
from ....db.session import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ....models.types.schemas import TypesRequest, TypesResponse
# from .auth import get_current_user

router = APIRouter(
    prefix="/types",
    tags=["Types"]
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
            response_model=list[TypesResponse],
            summary="List all Pokémon types",
            description="Retrieve all Pokémon types currently stored in the database.",
            status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    todos = db.query(Types).all()
    return todos

@router.post(    '/',
            status_code=status.HTTP_201_CREATED,
            response_model=TypesResponse,
            summary="Create a new Pokémon type",
            description="Adds a new Pokémon type to the database. The type name must be unique and in lowercase.")
async def create_type(db: db_dependency, type_request: TypesRequest):
    type_model = Types(**type_request.model_dump())

    type_found = db.query(Types).filter(Types.name.ilike(type_model.name)).first()

    if type_found:
        raise HTTPException(status_code=409, detail='Type already exists')

    db.add(type_model)
    db.commit()
    db.refresh(type_model)  # Refresh to get the ID and other generated fields
    return type_model


