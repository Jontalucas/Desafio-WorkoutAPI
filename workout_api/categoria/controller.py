from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.categoria.models import CategoriaModel
from workout_api.contrib.repository.dependencies import DataBaseDependency
from workout_api.categoria.schemas import CategoriaIn, CategoriaOut 
from sqlalchemy.future import select


router = APIRouter()

@router.post(path='/', summary="Adicionar Categoria", status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)
async def post(db_session: DataBaseDependency, categoria_insert: CategoriaIn = Body(...)) -> CategoriaOut:
    try:
        categoria_out = CategoriaOut(id=uuid4(), **categoria_insert.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())
        db_session.add(categoria_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma categoria com esse nome: {categoria_model.nome}'
        )
    
    return categoria_out

@router.get(path='/', summary="Consultar todas as Categorias", status_code=status.HTTP_200_OK, response_model=list[CategoriaOut])
async def get(db_session: DataBaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias


@router.get(path='/{id}', summary="Consultar categoria por id", status_code=status.HTTP_200_OK, response_model=CategoriaOut)
async def get(id: UUID4, db_session: DataBaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada nesse id")
    return categoria