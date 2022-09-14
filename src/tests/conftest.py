import pytest
from src.app import app

class Auth:
    def __init__(self, client):
        self._client = client

    def login(self, username):
        return self._client.post(
            f'/login?username={username}'
        )

    def logout(self):
        return self._client.get('/logout')

@pytest.fixture()
def client():
    return app.test_client()

@pytest.fixture
def auth(client):
    return Auth(client)