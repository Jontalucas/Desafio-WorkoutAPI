
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.contrib.repository.dependencies import DataBaseDependency
from workout_api.centro_treinamento.schemas import CTIn, CTOut
from workout_api.centro_treinamento.models import CTModel
from sqlalchemy.future import select

router = APIRouter()

@router.post(path='/', summary="Adicionar CT", status_code=status.HTTP_201_CREATED, response_model=CTOut)
async def post(db_session: DataBaseDependency, ct_insert: CTIn = Body(...)) -> CTOut:
    try:
        ct_out = CTOut(id=uuid4(), **ct_insert.model_dump())
        ct_model = CTModel(**ct_out.model_dump())
        db_session.add(ct_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um CT com esse nome: {ct_model.nome}'
        )
        
    return ct_out

@router.get(path='/', summary="Consultar todas os CTs", status_code=status.HTTP_200_OK, response_model=list[CTOut])
async def get(db_session: DataBaseDependency) -> list[CTOut]:
    cts: list[CTOut] = (await db_session.execute(select(CTModel))).scalars().all()
    return cts


@router.get(path='/{id}', summary="Consultar CT por id", status_code=status.HTTP_200_OK, response_model=CTOut)
async def get(id: UUID4, db_session: DataBaseDependency) -> CTOut:
    ct: CTOut = (await db_session.execute(select(CTModel).filter_by(id=id))).scalars().first()
    
    if not ct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CT não encontrado nesse id")
    return ct