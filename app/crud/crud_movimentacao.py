from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.conta import ContaCreate
from app.crud.base import CRUDBase


class CRUDConta(CRUDBase[Conta, ContaCreate]):
    def get_movimentacoes(self, db_session: Session, *, obj_in: Conta):
        pass


conta = CRUDConta(Conta)
