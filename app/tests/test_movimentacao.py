from fastapi.testclient import TestClient
from app.main import app
from app import crud
from app.core.database import SessionLocal
from app.schemas.conta import ContaCreate


client = TestClient(app)


def conta_fake(conta_id=False):
    if not conta_id:
        conta_in = ContaCreate()
        conta = crud.conta.create(
            db_session=SessionLocal(), obj_in=conta_in)
        return conta.id
    crud.conta.remove(db_session=SessionLocal(), id=conta_id)


def test_cria_movimentacao_deposito(conta_id=conta_fake()):
    j = {'conta_id': conta_id, 'valor': 100.0}
    response = client.post(url="/api/v1/movimentacao/deposito", json=j)
    res = response.json()
    assert response.status_code == 200
    assert res[0]['tipo'] == 'deposito'
    assert res[0]['valor'] == 100
    assert res[0]['saldo_conta_atual'] == 100
    assert res[1]['tipo'] == 'taxa'
    assert res[1]['valor'] == -1
    assert res[1]['saldo_conta_atual'] == 99
    conta_fake(conta_id)


def test_cria_movimentacao_saque(conta_id=conta_fake()):
    j = {'conta_id': conta_id, 'valor': 200.0}
    client.post(url="/api/v1/movimentacao/deposito", json=j)
    j = {'conta_id': conta_id, 'tipo': 'saque', 'valor': 100.0}
    response = client.post(url="/api/v1/movimentacao/saque", json=j)
    res = response.json()
    assert response.status_code == 200
    assert res[0]['tipo'] == j['tipo']
    assert res[0]['valor'] == -100
    assert res[0]['saldo_conta_atual'] == 98
    assert res[1]['tipo'] == 'taxa'
    assert res[1]['valor'] == -4
    assert res[1]['saldo_conta_atual'] == 94
    conta_fake(conta_id=conta_id)
