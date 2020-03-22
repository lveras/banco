from pydantic import BaseModel
from .movimentacao import Movimentacao, MovimentacaoTransferencia
from typing import List, Optional, Union


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
    movimentacoes: Union[List[Movimentacao], List[MovimentacaoTransferencia]] = None

    class Config:
        orm_mode = True


class ContaExtrato(Conta):
    saldo: float
