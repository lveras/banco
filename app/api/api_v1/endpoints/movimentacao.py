from fastapi import APIRouter, Depends, HTTPException
from app import crud
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import movimentacao
from typing import List

router = APIRouter()

TIPOS_MOVIMENTACAO = ['saque', 'deposito', 'transferencia']


@router.post("/", response_model=List[movimentacao.Movimentacao])
def create_deposito(*, db: Session = Depends(get_db),
                    movimentacao_in: movimentacao.MovimentacaoCreate):
    conta = crud.conta.get(db_session=db, id=movimentacao_in.conta_id)
    if not conta:
        raise HTTPException(status_code=422, detail="Conta não encontrada")
    if movimentacao_in.tipo not in TIPOS_MOVIMENTACAO:
        raise HTTPException(status_code=422, detail="Tipo inválido")
    return crud.movimentacao.create(db_session=db, obj_in=movimentacao_in)
