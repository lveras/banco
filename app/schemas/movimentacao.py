from pydantic import BaseModel


class MovimentacaoBase(BaseModel):
    tipo: str
    valor: float
    conta_id = int


class MovimentacaoCreate(MovimentacaoBase):
    pass


class MovimentacaoInDBBase(MovimentacaoBase):
    id: int

    class Config:
        orm_mode = True


class Movimentacao(MovimentacaoBase):
    pass
