from pydantic import BaseModel


class ContaBase(BaseModel):
    id: int = None


class Conta(ContaBase):
    pass
