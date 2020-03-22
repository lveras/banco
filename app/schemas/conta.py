from pydantic import BaseModel
from .movimentacao import Movimentacao
from typing import List


class ContaBase(BaseModel):
    pass


class ContaCreate(ContaBase):
    pass


class ContaInDBBase(ContaBase):
    id: int = None
    movimentacoes: List[Movimentacao] = None

    class Config:
        orm_mode = True


class Conta(ContaBase):
    id: int = None
    movimentacoes: List[Movimentacao] = None

    class Config:
        orm_mode = True


class ContaExtrato(Conta):
    saldo: float
