# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_tech.app import app
from fast_tech.db import Base  # Importe Base do db.py


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # Use banco de dados em memória para testes
    test_engine = create_engine('sqlite:///:memory:', echo=True)

    # Crie todas as tabelas
    Base.metadata.create_all(bind=test_engine)

    with Session(test_engine) as session:
        yield session

    # Limpe após os testes
    Base.metadata.drop_all(bind=test_engine)
