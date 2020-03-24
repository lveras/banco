from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreate

TAXAS = {
    'deposito': lambda x: (abs(x), -abs(x)*0.01, abs(x)-abs(x)*0.01),
    'saque': lambda x: (abs(x), -4, -(abs(x))-4),
    'transferencia': lambda x: (abs(x), -1, -(abs(x)+1)),
}


def calcula_taxa(obj_in: MovimentacaoCreate) -> MovimentacaoCreate:
    if obj_in.tipo == 'transferencia' and \
       obj_in.conta_destino_id == obj_in.conta_id:
        obj_in.taxa = 0
        obj_in.saldo_movimentacao = obj_in.valor
    else:
        vl, taxa, saldo_movimentacao = TAXAS[obj_in.tipo](obj_in.valor)
        obj_in.valor = vl
        obj_in.taxa = taxa
        obj_in.saldo_movimentacao = saldo_movimentacao
    return obj_in


class CRUDMovimentacao(CRUDBase[Movimentacao, MovimentacaoCreate]):
    def create(self, db_session: Session, *, obj_in: MovimentacaoCreate):
        res = []
        mov = calcula_taxa(obj_in=obj_in)
        obj = super(CRUDMovimentacao, self).create(
            db_session=db_session, obj_in=mov)
        saldo = round(
            sum([m.saldo_movimentacao for m in obj.conta.movimentacoes]), 2)
        obj.saldo_conta_atual = saldo
        obj.conta.saldo = saldo
        if obj_in.tipo == 'transferencia' and \
           obj_in.conta_origem_id == obj_in.conta_id:
            obj_in.conta_id = obj_in.conta_destino_id
            self.create(db_session=db_session, obj_in=obj_in)
        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)
        res.append(obj)
        return res


movimentacao = CRUDMovimentacao(Movimentacao)
