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
    taxa: float = None
    saldo_movimentacao: float = None


class Movimentacao(MovimentacaoBase):
    tipo: str
    valor: float
    taxa: float
    saldo_movimentacao: float
    saldo_conta_atual: float
    created_date: datetime


class MovimentacaoInDBBase(MovimentacaoBase):
    pass
