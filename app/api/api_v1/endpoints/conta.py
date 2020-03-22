from fastapi import APIRouter, Depends
from app import crud
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import conta
router = APIRouter()


@router.post("/", response_model=conta.Conta)
def create_conta(*, db: Session = Depends(get_db),
                 conta_in: conta.ContaCreate):
    return crud.conta.create(db_session=db, obj_in=conta_in)


@router.get("/extrato/{id}", response_model=conta.ContaExtrato)
def ver_extrato_conta(id: int, db: Session = Depends(get_db)):
    conta = crud.conta.get(db_session=db, id=id)
    return conta
