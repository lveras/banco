from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class MovimentacaoBase(BaseModel):
    valor: float

    class Config:
        orm_mode = True


class MovimentacaoCreate(MovimentacaoBase):
    conta_id: int
    tipo: str
    taxa: float = None
    saldo_movimentacao: float = None
    conta_origem_id: int = None
    conta_destino_id: int = None


class MovCreateSaqueDeposito(MovimentacaoBase):
    conta_id: int


class MovCreateTransferencia(MovimentacaoBase):
    conta_id: int
    conta_destino_id: int


class Movimentacao(MovimentacaoBase):
    tipo: str
    valor: float
    taxa: float
    saldo_movimentacao: float
    saldo_conta_atual: float
    created_date: datetime


class MovimentacaoTransferencia(Movimentacao):
    conta_origem_id: int
    conta_destino_id: int


class MovimentacaoInDBBase(MovimentacaoBase):
    pass
