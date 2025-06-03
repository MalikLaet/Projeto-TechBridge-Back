from sqlalchemy import select

from fast_tech.models import User


def test_create_user(session):
    # Teste de criação
    new_user = User(
        name='Test User',
        username='testuser',
        email='test@example.com',
        phone='(11)99999-9999',
        password='secret',
    )
    session.add(new_user)
    session.commit()

    # Teste de consulta
    user = session.scalar(select(User).where(User.username == 'testuser'))

    assert user is not None
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
