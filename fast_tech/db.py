from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Exemplo com SQLite. Troque pela sua URL do banco (Postgres, MySQL, etc.)
DATABASE_URL = 'sqlite:///./db.sqlite3'

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
