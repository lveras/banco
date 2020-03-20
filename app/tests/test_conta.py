from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_cria_conta():
    response = client.post("/api/v1/conta/", json={})
    data = response.json()
    assert response.status_code == 200
    assert 'id' in data
    assert 'movimentacoes' in data
    assert type(data['movimentacoes']) is list
