from pydantic import BaseModel
from datetime import datetime


class MovimentacaoBase(BaseModel):
    valor: float = None

    class Config:
        orm_mode = True


class MovimentacaoCreate(MovimentacaoBase):
    conta_id: int = None


class MovimentacaoCreateTipo(MovimentacaoCreate):
    tipo: str = None


class Movimentacao(MovimentacaoBase):
    tipo: str = None
    valor: float = None
    saldo_conta_atual: float = None
    created_date: datetime = None


class MovimentacaoInDBBase(MovimentacaoBase):
    pass
