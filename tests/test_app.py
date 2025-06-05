import uuid
from http import HTTPStatus

from fastapi.testclient import TestClient
from passlib.context import CryptContext

from fast_tech.app import app

client = TestClient(app)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def test_create_user():
    client = TestClient(app)

    unique_username = f'malik_{uuid.uuid4().hex[:6]}'
    unique_email = f'{unique_username}@test.com'

    response = client.post(
        '/registerStudent',
        json={
            'name': unique_username,
            'username': unique_username,
            'email': unique_email,
            'phone': '(11)929038780',
            'password': 'secret',
        },
    )
    if response.status_code != HTTPStatus.CREATED:
        print('Erro:', response.status_code, response.json())

    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert 'id' in response_json
    assert response_json['username'] == unique_username
    assert response_json['email'] == unique_email
