from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from fast_tech.db import Base, SessionLocal, engine
from fast_tech.models import User
from fast_tech.schema import UserPublic, UserSchema
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # Seu frontend React
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # Permite todos os headers
)

# Cria tabelas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    '/registerStudent', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def create_user(
    user: UserSchema,
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail='Username já existe')

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail='Email já existe')

    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        password=user.password,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user  # ✅ Agora retorna o objeto do usuário criado

@app.get("/usuarios", response_model=List[UserPublic])
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Retorna todos os usuários cadastrados no sistema
    """
    usuarios = db.query(User).all()
    return usuarios