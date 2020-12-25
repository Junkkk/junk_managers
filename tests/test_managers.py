import sys
sys.path = ['', '..'] + sys.path[1:]


from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_managers_list():
    response = client.get('/managers')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'
