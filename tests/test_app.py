from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_tech.app import app

client = TestClient(app)


def test_create_user_deve_retornar_sucesso():
    payload = {
        'name': 'Maria Silva',
        'username': 'mariasilva',
        'email': 'maria@gmail.com',
        'telefone': '11987654321',
        'password': 'senha123',
    }

    response = client.post('/cadastrar', json=payload)

    assert response.status_code == HTTPStatus.OK

    # Verifica que existe o message
    assert response.json()['message'] == 'Usuário criado com sucesso'

    # E verifica que user_id está presente e é um número inteiro
    assert isinstance(response.json()['user_id'], int)


# def test_create_user_username_ja_existente():
#     payload = {
#         'name': 'Maria Silva',
#         'username': 'mariasilva',
#         'email': 'maria@gmail.com',
#         'telefone': '11987654321',
#         'password': 'senha123',
#     }

#     response = client.post('/cadastrar', json=payload)

#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json()['detail'] == 'Username já existe'


# def test_create_user_email_ja_existente():
#     payload = {
#         'name': 'Maria Silva',
#         'username': 'mariasilva',
#         'email': 'maria@gmail.com',
#         'telefone': '11987654321',
#         'password': 'senha123',
#     }

#     response = client.post('/cadastrar', json=payload)

#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json()['detail'] == 'Email já existe'
