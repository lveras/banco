from sqlalchemy.orm import Session

from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreateTipo
from app.crud.base import CRUDBase

TAXAS = {
    'deposito': lambda x: (abs(x), -abs(x)*0.01, abs(x)-abs(x)*0.01),
    'saque': lambda x: (abs(x), -4, -(abs(x)-4)),
    'transferencia': lambda x: (abs(x), -1, abs(x)-1),
}


class CRUDMovimentacao(CRUDBase[Movimentacao, MovimentacaoCreateTipo]):
    def create(self, db_session: Session, *, obj_in: MovimentacaoCreateTipo):
        res = []
        vl, taxa, saldo_movimentacao = TAXAS[obj_in.tipo](obj_in.valor)
        mov = MovimentacaoCreateTipo(
            conta_id=obj_in.conta_id, tipo=obj_in.tipo,
            valor=vl, taxa=taxa, saldo_movimentacao=saldo_movimentacao)
        obj = super(CRUDMovimentacao, self).create(
            db_session=db_session, obj_in=mov)
        saldo = round(sum([m.saldo_movimentacao
                           for m in obj.conta.movimentacoes]), 2)
        obj.saldo_conta_atual = saldo
        obj.conta.saldo = saldo
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        res.append(obj)
        return res


movimentacao = CRUDMovimentacao(Movimentacao)
