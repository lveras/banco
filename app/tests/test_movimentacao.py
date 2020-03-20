from fastapi.testclient import TestClient
from app.main import app
from app import crud
from app.core.database import SessionLocal
from app.schemas.conta import ContaCreate


client = TestClient(app)


def conta_fake(func):
    def log():
        def wrapped():
            conta_in = ContaCreate()
            conta = crud.conta.create(
                db_session=SessionLocal(), obj_in=conta_in)
            func(conta.id)
            crud.conta.remove(db_session=SessionLocal(), id=conta.id)
        return wrapped
    return log


@conta_fake
def test_cria_movimentacao_deposito(conta_id):
    j = {'conta_id': conta_id, 'tipo': 'deposito', 'valor': 100.0}
    response = client.post(url="/api/v1/movimentacao/deposito", json=j)
    res = response.json()
    assert response.status_code == 200
    assert res[0]['tipo'] == j['tipo']
    assert res[0]['valor'] == 100
    assert res[0]['saldo_conta_atual'] == 100
    assert res[1]['tipo'] == 'taxa'
    assert res[1]['valor'] == 1
    assert res[1]['saldo_conta_atual'] == 99
