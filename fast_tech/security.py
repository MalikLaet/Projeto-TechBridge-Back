from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = 'sua_chave_super_secreta'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_student(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload or payload.get('role') != 'student':
        raise HTTPException(
            status_code=403,
            detail='Acesso negado: apenas estudantes autorizados.',
        )
    return payload


def get_current_company(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload or payload.get('role') != 'company':
        raise HTTPException(
            status_code=403,
            detail='Acesso negado: apenas empresas autorizadas.',
        )
    return payload
