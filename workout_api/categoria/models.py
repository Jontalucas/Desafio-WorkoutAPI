from sqlalchemy import Integer, String
from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship




class CategoriaModel(BaseModel):
    __tablename__ = 'categoria'
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    atletas: Mapped['AtletasModel'] = relationship(back_populates='categoria')