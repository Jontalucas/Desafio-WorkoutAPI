from datetime import datetime
#from datetime import UTC
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CTModel
from workout_api.contrib.repository.dependencies import DataBaseDependency
from workout_api.atletas.schemas import AtletaIn, AtletaOut, AtletaShow, AtletaUpdate
from workout_api.atletas.models import AtletasModel
from sqlalchemy.exc import IntegrityError 

router = APIRouter()

@router.post(path='/', summary="Adicionar Atleta", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DataBaseDependency, atleta_insert: AtletaIn = Body(...)):
    
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_insert.categoria.nome))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria não encontrada")
    
    centro_treinamento = (await db_session.execute(select(CTModel).filter_by(nome=atleta_insert.centro_treinamento.nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CT não encontrada")
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_insert.model_dump())
        atleta_model = AtletasModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_model.cpf}'
        )

    return atleta_out

@router.get(path='/', summary="Consultar todas os Atletas", status_code=status.HTTP_200_OK, response_model=list[AtletaShow])
async def get_all(db_session: DataBaseDependency) -> list[AtletaShow]:
    
    atletas: list[AtletaShow] = (await db_session.execute(select(AtletasModel))).scalars().all()
    return atletas

@router.get(path='/{id}', summary="Consultar um atleta por id", status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def get(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado nesse id")
    return atleta

@router.get(path='/cpf/', summary="Consultar um atleta por cpf", status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def get(cpf: str, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(cpf=cpf))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado nesse CPF")
    return atleta

@router.get(path='/nome/', summary="Consultar um atleta por nome", status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def get(nome: str, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(nome=nome))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado nesse CPF")
    return atleta


@router.patch(path='/{id}', summary="Editar um atleta por id", status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def patch(id: UUID4, db_session: DataBaseDependency, atleta_update: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado nesse id")
    atleta_up = atleta_update.model_dump(exclude_unset= True)
    for key, value in atleta_up.items():
        setattr(atleta, key, value)
    
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

@router.delete(path='/{id}', summary="Deletar um atleta por id", status_code=status.HTTP_204_NO_CONTENT)
async def get(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado nesse id")
    
    await db_session.delete(atleta)
    await db_session.commit()
    
