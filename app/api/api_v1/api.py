from fastapi import APIRouter
from app.api.api_v1.endpoints import conta, movimentacao

api_router = APIRouter()
api_router.include_router(conta.router, prefix="/conta", tags=["conta"])
api_router.include_router(
    movimentacao.router, prefix="/movimentacao", tags=["movimentacao"])
