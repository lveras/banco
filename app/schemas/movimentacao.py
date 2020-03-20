from pydantic import BaseModel
from datetime import datetime


class MovimentacaoBase(BaseModel):
    tipo: str = None
    valor: float = None

    class Config:
        orm_mode = True


class MovimentacaoCreate(MovimentacaoBase):
    conta_id: int = None


class Movimentacao(MovimentacaoBase):
    conta_id: int = None
    created_date: datetime = None


class MovimentacaoInDBBase(MovimentacaoBase):
    pass
