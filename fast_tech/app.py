from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from fast_tech.db import Base, SessionLocal, engine
from fast_tech.models import Company, Curso, Inscricao, User
from fast_tech.schema import (
    CompanyLogin,
    CompanyOut,
    CompanySchema,
    CursoCreate,
    CursoEmpresaOut,
    InscricaoCreate,
    LoginResponse,
    UserLogin,
    UserPublic,
    UserSchema,
)
from fast_tech.security import (
    create_access_token,
    get_current_company,
    get_current_student
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
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
        access_token = create_access_token({
            'sub': db_user.username,
            'role': 'student',
            'id': db_user.id,
        })
        return {
            'message': 'Login bem sucedido',
            'id': db_user.id,
            'username': db_user.username,
            'email': db_user.email,
            'token': access_token,
        }

    except Exception as e:
        print(f'Erro durante o login: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro durante o login',
        )


@app.post(
    '/registerCompany',
    status_code=HTTPStatus.CREATED,
    response_model=CompanyOut,
)
def create_company(
    company: CompanySchema,
    db: Session = Depends(get_db),
):
    if db.query(Company).filter(Company.username == company.username).first():
        raise HTTPException(status_code=400, detail='Username já existe')

    if db.query(Company).filter(Company.email == company.email).first():
        raise HTTPException(status_code=400, detail='Email já existe')

    if db.query(Company).filter(Company.cnpj == company.cnpj).first():
        raise HTTPException(status_code=400, detail='CNPJ já cadastrado')

    hashed_password = pwd_context.hash(company.password)

    db_company = Company(
        cnpj=company.cnpj,
        username=company.username,
        email=company.email,
        password=hashed_password,
        phone=company.phone,
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


@app.post(
    '/companyLogin',
    status_code=HTTPStatus.OK,
    response_model=LoginResponse,
    responses={
        404: {'description': 'Usuário não encontrado'},
        400: {'description': 'Credenciais inválidas'},
        500: {'description': 'Erro interno no servidor'},
    },
)
async def login_company(
    user: CompanyLogin,
    db: Session = Depends(get_db),
):
    try:
        db_company = (
            db.query(Company).filter(Company.username == user.username).first()
        )

        if not db_company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuário não encontrado',
            )

        if not pwd_context.verify(user.password, db_company.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Credenciais inválidas',
            )

        return {
            'message': 'Login bem-sucedido',
            'id': db_company.id,
            'username': db_company.username,
            'email': db_company.email,
        }
    except Exception as e:
        print(f'Erro durante o login: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro durante o login',
        )


@app.post('/createCourses')
def criar_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    # Verifique se a empresa existe
    empresa = db.query(Company).filter(Company.id == curso.company_id).first()

    if not empresa:
        print(f'Empresa com ID {curso.company_id} não encontrada')
        raise HTTPException(
            status_code=404,
            detail=f'Empresa com ID {curso.company_id} não encontrada',
        )

    # Crie o curso
    novo_curso = Curso(
        name=curso.name,
        description=curso.description,
        youtube_link=curso.youtube_link,
        company_id=curso.company_id,
    )

    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)

    return {'message': 'Curso criado com sucesso', 'company_id': novo_curso.id}


@app.get(
    '/companies/{company_id}/courses', response_model=List[CursoEmpresaOut]
)
def list_company_courses(company_id: int, db: Session = Depends(get_db)):
    courses = db.query(Curso).filter(Curso.company_id == company_id).all()

    if not courses:
        raise HTTPException(
            status_code=404, detail='No courses found for this company.'
        )

    return courses


@app.get('/courses', response_model=List[CursoEmpresaOut])
def list_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Curso).join(Company).all()

    if not courses:
        raise HTTPException(status_code=404, detail='No courses found')

    return courses


@app.get('/courses/{curso_id}')
def get_course(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail='Curso não encontrado.')
    return curso


@app.post('/enrollments', status_code=status.HTTP_201_CREATED)
def create_enrollment(
    inscricao: InscricaoCreate, db: Session = Depends(get_db)
):
    curso = db.query(Curso).filter(Curso.id == inscricao.course_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail='Curso não encontrado.')

    aluno = db.query(User).filter(User.id == inscricao.student_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail='Aluno não encontrado.')

    ja_inscrito = (
        db.query(Inscricao)
        .filter(
            Inscricao.student_id == inscricao.student_id,
            Inscricao.course_id == inscricao.course_id,
        )
        .first()
    )

    if ja_inscrito:
        raise HTTPException(
            status_code=409, detail='Aluno já está inscrito nesse curso.'
        )

    nova_inscricao = Inscricao(
        student_id=inscricao.student_id, course_id=inscricao.course_id
    )

    db.add(nova_inscricao)
    db.commit()
    db.refresh(nova_inscricao)

    return {
        'message': 'Inscrição realizada com sucesso',
        'enrollment_id': nova_inscricao.id,
    }


@app.get('/students/my-courses', response_model=List[CursoEmpresaOut])
def listar_cursos_aluno(user_id: int, db: Session = Depends(get_db)):
    inscricoes = (
        db.query(Inscricao).filter(Inscricao.student_id == user_id).all()
    )

    if not inscricoes:
        return []

    cursos_ids = [inscricao.course_id for inscricao in inscricoes]
    cursos = db.query(Curso).filter(Curso.id.in_(cursos_ids)).all()

    if not cursos:
        raise HTTPException(
            status_code=404, detail='Nenhum curso encontrado para o aluno.'
        )

    return cursos


@app.delete(
    '/companies/my-courses/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Curso excluído com sucesso'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Curso não pertence à empresa'},
        404: {'description': 'Curso não encontrado'},
        409: {
            'description': 'Curso tem alunos inscritos e não pode ser excluído'
        },
    },
)
@app.delete(
    '/companies/my-courses/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Curso excluído com sucesso'},
    },
)
def delete_course(
    course_id: int,
    current_company = Depends(get_current_company),
    db: Session = Depends(get_db),
):
    curso = db.query(Curso).filter(Curso.id == course_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail='Curso não encontrado.')

    if curso.company_id != current_company:
        raise HTTPException(
            status_code=403, detail='Curso não pertence à empresa logada.'
        )

    if db.query(Inscricao).filter(Inscricao.course_id == course_id).first():
        raise HTTPException(
            status_code=409,
            detail='Curso possui alunos inscritos e não pode ser excluído.',
        )

    db.delete(curso)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
