from sqlalchemy.orm import Session

from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreateTipo
from app.crud.base import CRUDBase

TAXAS = {
    'deposito': lambda x: (x*0.01, x*0.99),
    'saque': lambda x: (x-4, 4),
    'transferencia': lambda x: (x-1, 1),
}


class CRUDMovimentacao(CRUDBase[Movimentacao, MovimentacaoCreateTipo]):
    def create(self, db_session: Session, *, obj_in: MovimentacaoCreateTipo):
        res = []
        taxa, valor = TAXAS[obj_in.tipo](obj_in.valor)
        taxa = MovimentacaoCreateTipo(
            conta_id=obj_in.conta_id, tipo='taxa', valor=taxa)
        mov = MovimentacaoCreateTipo(
            conta_id=obj_in.conta_id, tipo=obj_in.tipo, valor=valor)
        res.append(super(CRUDMovimentacao, self).create(
            db_session=db_session, obj_in=mov))
        res.append(super(CRUDMovimentacao, self).create(
            db_session=db_session, obj_in=taxa))
        return res


movimentacao = CRUDMovimentacao(Movimentacao)
