from fastapi import APIRouter, Depends
from app import crud
from sqlalchemy.orm import Session
from app.api.api_v1.utils.db import get_db
from app.schemas.conta import Conta
from app.models.conta import Conta as DBConta
router = APIRouter()


@router.post("/conta/{id}", response_model=Conta)
def ver_conta(id: int, db: Session = Depends(get_db)):
    ...
