from fastapi.testclient import TestClient
from app.main import app
from app.tests.test_movimentacao import conta_fake
client = TestClient(app)
ID_CONTA = ''


def test_cria_conta():
    response = client.post(url="/api/v1/conta/", json={})
    data = response.json()
    assert response.status_code == 200
    assert 'id' in data
    assert 'movimentacoes' in data
    assert type(data['movimentacoes']) is list


@conta_fake
def test_pega_extrato_da_conta(conta_id):
    j = {'conta_id': conta_id, 'tipo': 'deposito', 'valor': 100.0}
    client.post(url="/api/v1/movimentacao/deposito", json=j)
    j = {'conta_id': conta_id, 'tipo': 'deposito', 'valor': 200.0}
    client.post(url="/api/v1/movimentacao/deposito", json=j)
    response = client.get(
        url="/api/v1/conta/extrato/{}".format(conta_id))

    data = response.json()
    assert response.status_code == 200
    assert 'id' in data
    assert 'movimentacoes' in data
    assert type(data['movimentacoes']) is list
