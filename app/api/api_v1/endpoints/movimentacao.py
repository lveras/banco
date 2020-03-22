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


@router.post('/deposito', response_model=List[movimentacao.Movimentacao])
def create_deposito(*, db: Session = Depends(get_db),
                    movimentacao_in: movimentacao.MovimentacaoCreate):
    verifica_conta(conta_id=movimentacao_in.conta_id, db=db)
    mov_in = movimentacao.MovimentacaoCreateTipo(
        valor=movimentacao_in.valor,
        conta_id=movimentacao_in.conta_id,
        tipo='deposito',
    )
    return crud.movimentacao.create(db_session=db, obj_in=mov_in)


@router.post('/saque', response_model=List[movimentacao.Movimentacao])
def create_saque(*, db: Session = Depends(get_db),
                 movimentacao_in: movimentacao.MovimentacaoCreate):
    verifica_conta(conta_id=movimentacao_in.conta_id, db=db)
    saldo = crud.conta.ver_saldo(db_session=db, id=movimentacao_in.conta_id)
    if saldo < movimentacao_in.valor:
        raise HTTPException(status_code=422, detail="Saldo insuficiente")
    mov_in = movimentacao.MovimentacaoCreateTipo(
        valor=movimentacao_in.valor,
        conta_id=movimentacao_in.conta_id,
        tipo='saque',
    )
    return crud.movimentacao.create(db_session=db, obj_in=mov_in)
