from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fast_tech.db import SessionLocal, engine
from fast_tech.models import User, table_registry
from fast_tech.schema import UserSchema, UserPublic

# Cria as tabelas no banco
table_registry.metadata.create_all(bind=engine)

app = FastAPI()


# Dependência para abrir e fechar conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/cadastrar')
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Verificar se já existe username ou email
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail='Username já existe')

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail='Email já existe')

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,  # ⚠️ ideal fazer hash da senha aqui
        telefone=user.telefone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {'message': 'Usuário criado com sucesso', 'user_id': db_user.id}


from typing import List

@app.get('/usuarios', response_model=List[UserPublic])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
