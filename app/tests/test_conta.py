from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
ID_CONTA = ''


def test_cria_conta():
    response = client.post(url="/api/v1/conta/", json={})
    data = response.json()
    assert response.status_code == 200
    assert 'id' in data
    assert 'movimentacoes' in data
    assert type(data['movimentacoes']) is list


def test_lista_conta_pelo_id():
    c = client.post(url="/api/v1/conta/", json={})
    response = client.get(url="/api/v1/conta/{}".format(c.json()['id']))
    data = response.json()
    assert response.status_code == 200
    assert 'id' in data
    assert 'movimentacoes' in data
    assert type(data['movimentacoes']) is list
