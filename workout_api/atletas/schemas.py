from typing import Annotated
from pydantic import Field, PositiveFloat
from workout_api.categoria.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CTAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do Atleta', max_length=11)]
    idade: Annotated[int, Field(description='Idade do Atleta')]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta')]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta')]
    sexo: Annotated[str, Field(description='Sexo do Atleta', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[CTAtleta, Field(description='Centro de Treinamento do Atleta')]
    
class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', max_length=50, nullable=True)]
    idade: Annotated[int, Field(description='Idade do Atleta')]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta')]
    
class AtletaShow(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[CTAtleta, Field(description='Centro de Treinamento do Atleta')]