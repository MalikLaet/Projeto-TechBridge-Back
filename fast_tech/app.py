from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from fast_tech.db import Base, SessionLocal, engine
from fast_tech.models import User
from fast_tech.schema import LoginResponse, UserLogin, UserPublic, UserSchema

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Cria tabelas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


@app.post(
    '/registerStudent',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
def create_user(
    user: UserSchema,
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail='Username já existe')

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail='Email já existe')

    hashed_password = pwd_context.hash(user.password)

    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get('/usuarios', response_model=List[UserPublic])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(User).all()
    return usuarios


@app.post(
    '/login',
    status_code=HTTPStatus.OK,
    response_model=LoginResponse,
    responses={
        404: {'description': 'Usuário não encontrado'},
        400: {'description': 'Credenciais inválidas'},
        500: {'description': 'Erro interno no servidor'},
    },
)
async def login_student(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuário não encontrado',
            )

        if not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Credenciais inválidas',
            )

        return {
            'message': 'Login bem-sucedido',
            'username': db_user.username,
        }

    except Exception as e:
        print(f'Erro durante o login: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro durante o login',
        )
