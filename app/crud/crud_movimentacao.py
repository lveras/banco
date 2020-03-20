from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreate
from app.crud.base import CRUDBase


class CRUDConta(CRUDBase[Movimentacao, MovimentacaoCreate]):
    def get_movimentacoes(self, db_session: Session, *, obj_in: Movimentacao):
        pass


movimentacao = CRUDConta(Movimentacao)
