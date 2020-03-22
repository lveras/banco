from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.conta import ContaCreate
from app.crud.base import CRUDBase


class CRUDConta(CRUDBase[Conta, ContaCreate]):
    def ver_saldo(self, db_session: Session, *, id: int):
        return self.get(db_session=db_session, id=id).saldo


conta = CRUDConta(Conta)
