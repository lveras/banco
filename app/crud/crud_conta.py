from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.conta import ContaCreate
from app.crud.base import CRUDBase


class CRUDConta(CRUDBase[Conta, ContaCreate]):
    def get_saldo(self, db_session: Session, *, id: int):
        pass


conta = CRUDConta(Conta)
