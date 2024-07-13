from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome da CT', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do CT', max_length=60)]
    proprietario: Annotated[str, Field(description='Nome do Proprietario do CT', max_length=30)]
    
class CTIn(CentroTreinamento):
    pass

class CTAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome da CT', max_length=20)]

class CTOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description='Identificador ddo CT')]
    nome: Annotated[str, Field(description='Nome do CT')]
    endereco: Annotated[str, Field(description='Endereço do CT')]
    proprietario: Annotated[str, Field(description='Proprietario do CT')]