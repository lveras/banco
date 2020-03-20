from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_cria_deposito():
    c = client.post(url="/api/v1/conta/", json={})
    id_conta = c.json()['id']
    j = {'id': id_conta, 'tipo': 'deposito', 'valor': 100.0}
    response = client.post(url="/api/v1/deposito/", json=j)
    assert response.status_code == 200
