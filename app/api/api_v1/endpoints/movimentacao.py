from fastapi import APIRouter, Depends
from app import crud
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import movimentacao
router = APIRouter()


@router.post("/", response_model=conta.Conta)
def create_deposito(*, db: Session = Depends(get_db),
                    movimentacao_in: conta.ContaCreate):
    return crud.conta.create(db_session=db, obj_in=movimentacao_in)
