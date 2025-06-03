from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

# CORRIJA A STRING DE CONEXÃO (adicione 3 barras para SQLite)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'  # Note as 3 barras

# Crie a engine com a URL corrigida
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},  # Importante para SQLite
    echo=True,
    future=True,
)

mapper_registry = registry()
Base = mapper_registry.generate_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
