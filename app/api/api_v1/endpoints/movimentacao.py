from fastapi import APIRouter, Depends, HTTPException
from app import crud
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import movimentacao
from typing import List

router = APIRouter()


def verifica_conta(conta_id: int, db):
    conta = crud.conta.get(db_session=db, id=conta_id)
    if not conta:
        raise HTTPException(status_code=422, detail="Conta nao encontrada")


def verifica_saldo(conta_id: int, valor: float, db):
    saldo = crud.conta.ver_saldo(db_session=db, id=conta_id)
    if saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")


@router.post('/deposito', response_model=List[movimentacao.Movimentacao])
def create_deposito(*, db: Session = Depends(get_db),
                    movimentacao_in: movimentacao.MovCreateSaqueDeposito):
    verifica_conta(conta_id=movimentacao_in.conta_id, db=db)
    mov = movimentacao.MovimentacaoCreate(
        conta_id=movimentacao_in.conta_id,
        valor=movimentacao_in.valor,
        tipo='deposito'
    )
    return crud.movimentacao.create(db_session=db, obj_in=mov)


@router.post('/saque', response_model=List[movimentacao.Movimentacao])
def create_saque(*, db: Session = Depends(get_db),
                 movimentacao_in: movimentacao.MovCreateSaqueDeposito):
    verifica_conta(conta_id=movimentacao_in.conta_id, db=db)
    verifica_saldo(conta_id=movimentacao_in.conta_id,
                   valor=movimentacao_in.valor, db=db)
    mov = movimentacao.MovimentacaoCreate(
        conta_id=movimentacao_in.conta_id,
        valor=movimentacao_in.valor,
        tipo='saque'
    )
    return crud.movimentacao.create(db_session=db, obj_in=mov)


@router.post('/transferencia', response_model=List[
                 movimentacao.MovimentacaoTransferencia])
def create_transferencia(*, db: Session = Depends(get_db),
                         movimentacao_in: movimentacao.MovCreateTransferencia):
    if movimentacao_in.conta_destino_id == movimentacao_in.conta_id:
        raise HTTPException(
            status_code=400, detail="Movimentacao nao permitida")
    verifica_conta(conta_id=movimentacao_in.conta_id, db=db)
    verifica_conta(conta_id=movimentacao_in.conta_destino_id, db=db)
    verifica_saldo(conta_id=movimentacao_in.conta_id,
                   valor=movimentacao_in.valor, db=db)
    mov = movimentacao.MovimentacaoCreate(
        conta_id=movimentacao_in.conta_id,
        valor=movimentacao_in.valor,
        conta_origem_id=movimentacao_in.conta_id,
        conta_destino_id=movimentacao_in.conta_destino_id,
        tipo='transferencia'
    )
    return crud.movimentacao.create(db_session=db, obj_in=mov)
