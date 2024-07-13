from fastapi import APIRouter
from workout_api.atletas.controller import router as atletas
from workout_api.categoria.controller import router as categoria
from workout_api.centro_treinamento.controller import router as ct

api_router = APIRouter()
api_router.include_router(atletas, prefix='/atletas', tags=['atletas/'])
api_router.include_router(categoria, prefix='/categoria', tags=['categoria/'])
api_router.include_router(ct, prefix='/ct', tags=['ct/'])
