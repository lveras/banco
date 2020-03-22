from fastapi.testclient import TestClient
from app.main import app
from app import crud
from app.core.database import SessionLocal
from app.schemas.conta import ContaCreate
from app.models.conta import Conta

client = TestClient(app)


def conta_fake(conta: Conta = False):
    if not conta:
        conta_in = ContaCreate()
        conta = crud.conta.create(
            db_session=SessionLocal(), obj_in=conta_in)
        return conta
    crud.conta.remove(db_session=SessionLocal(), id=conta.id)


def test_cria_movimentacao_conta_nao_encontrada():
    j = {'conta_id': 0, 'valor': 100.0}
    response = client.post(url="/api/v1/movimentacao/deposito", json=j)
    res = response.json()
    assert response.status_code == 422
    assert res['detail'] == 'Conta nao encontrada'


def test_cria_movimentacao_deposito(conta=conta_fake()):
    j = {'conta_id': conta.id, 'valor': 100.0}
    response = client.post(url="/api/v1/movimentacao/deposito", json=j)
    res = response.json()
    assert response.status_code == 200
    assert res[0]['tipo'] == 'deposito'
    assert res[0]['valor'] == 100
    assert res[0]['taxa'] == -1
    assert res[0]['saldo_movimentacao'] == 99
    assert res[0]['saldo_conta_atual'] == 99
    conta_fake(conta)


def test_cria_movimentacao_saque(conta=conta_fake()):
    j = {'conta_id': conta.id, 'valor': 200.0}
    client.post(url="/api/v1/movimentacao/deposito", json=j)
    j = {'conta_id': conta.id, 'tipo': 'saque', 'valor': 100.0}
    response = client.post(url="/api/v1/movimentacao/saque", json=j)
    res = response.json()
    assert response.status_code == 200
    assert res[0]['tipo'] == j['tipo']
    assert res[0]['valor'] == 100
    assert res[0]['taxa'] == -4
    assert res[0]['saldo_movimentacao'] == -104
    assert res[0]['saldo_conta_atual'] == 94
    conta_fake(conta=conta)


def test_cria_movimentacao_saque_saldo_insuficiente(conta=conta_fake()):
    j = {'conta_id': conta.id, 'valor': 200.0}
    client.post(url="/api/v1/movimentacao/deposito", json=j)
    j = {'conta_id': conta.id, 'tipo': 'saque', 'valor': 200.0}
    response = client.post(url="/api/v1/movimentacao/saque", json=j)
    res = response.json()
    assert response.status_code == 400
    assert res['detail'] == 'Saldo insuficiente'
    conta_fake(conta=conta)


def test_movimentacao_entre_contas(
        conta_origem_id=conta_fake(), conta_destino_id=conta_fake()):
    j = {'conta_id': conta_origem_id.id, 'valor': 200}
    client.post(url="/api/v1/movimentacao/deposito", json=j)
    j = {'conta_id': conta_origem_id.id, 'valor': 100,
         'conta_destino_id': conta_destino_id.id}
    response = client.post(url="/api/v1/movimentacao/transferencia", json=j)
    res = response.json()
    assert res[0]['tipo'] == 'transferencia'
    assert res[0]['conta_origem_id'] == conta_origem_id.id
    assert res[0]['conta_destino_id'] == conta_destino_id.id
    assert res[0]['valor'] == 100
    assert res[0]['taxa'] == -1
    assert res[0]['saldo_movimentacao'] == -101
    assert res[0]['saldo_conta_atual'] == 97
    assert crud.conta.ver_saldo(
        db_session=SessionLocal(),
        id=conta_destino_id.id) == 100
    conta_fake(conta_destino_id)
    conta_fake(conta_origem_id)


def test_movimentacao_transferencia_mesma_conta(conta=conta_fake()):
    j = {'conta_id': conta.id, 'valor': 200}
    client.post(url="/api/v1/movimentacao/deposito", json=j)
    j = {'conta_id': conta.id, 'valor': 100,
         'conta_destino_id': conta.id}
    response = client.post(url="/api/v1/movimentacao/transferencia", json=j)
    res = response.json()
    assert response.status_code == 400
    assert res['detail'] == 'Movimentacao nao permitida'
