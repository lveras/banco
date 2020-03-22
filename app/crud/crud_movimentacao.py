from sqlalchemy.orm import Session

from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreateTipo
from app.crud.base import CRUDBase

TAXAS = {
    'deposito': lambda x: (x, -x*0.01),
    'saque': lambda x: (-(abs(x)-4), -4),
    'transferencia': lambda x: (x, -1),
}


class CRUDMovimentacao(CRUDBase[Movimentacao, MovimentacaoCreateTipo]):
    def create(self, db_session: Session, *, obj_in: MovimentacaoCreateTipo):
        res = []
        vl, taxa = TAXAS[obj_in.tipo](obj_in.valor)
        for val in [obj_in.tipo, 'taxa']:
            mov = MovimentacaoCreateTipo(
                conta_id=obj_in.conta_id, tipo=val,
                valor=taxa if val == 'taxa' else vl)
            obj = super(CRUDMovimentacao, self).create(
                db_session=db_session, obj_in=mov)
            saldo = round(sum([m.valor for m in obj.conta.movimentacoes]), 2)
            obj.saldo_conta_atual = saldo
            obj.conta.saldo = saldo
            db_session.add(obj)
            db_session.commit()
            db_session.refresh(obj)
            res.append(obj)
        return res


movimentacao = CRUDMovimentacao(Movimentacao)
