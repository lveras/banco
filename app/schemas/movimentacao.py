from pydantic import BaseModel
from datetime import date


class MovimentacaoBase(BaseModel):
    tipo: str = None
    valor: float = None

    class Config:
        orm_mode = True


class MovimentacaoCreate(MovimentacaoBase):
    conta_id: int = None
    pass


class Movimentacao(MovimentacaoBase):
    conta_id: int = None
    created_date: date = None
    pass


class MovimentacaoInDBBase(MovimentacaoBase):
    pass
