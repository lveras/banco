from fastapi.testclient import TestClient
from fastapi import Depends
from app.main import app
from app import crud
from app.core.database import SessionLocal
from app.schemas.conta import ContaCreate

client = TestClient(app)


def test_cria_movimentacao_deposito():
    conta_in = ContaCreate()
    conta = crud.conta.create(db_session=SessionLocal(), obj_in=conta_in)
    j = {'conta_id': conta.id, 'tipo': 'deposito', 'valor': 100.0}
    response = client.post(url="/api/v1/movimentacao/", json=j)
    assert response.status_code == 200
    assert j['tipo'] == response.json()['tipo']
    assert j['valor'] == response.json()['valor']
    crud.conta.remove(db_session=SessionLocal(), id=conta.id)
