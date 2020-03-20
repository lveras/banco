from pydantic import BaseModel


class MovimentacaoBase(BaseModel):
    pass


class MovimentacaoCreate(MovimentacaoBase):
    pass


class MovimentacaoInDBBase(MovimentacaoBase):
    id: int = None


class Movimentacao(MovimentacaoBase):
    tipo: str = None
    valor: float = None
    conta_id: int = None

    class Config:
        orm_mode = True
    pass
