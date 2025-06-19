from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    phone: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    phone: str

    class Config:
        from_attributes = True


class UserDB(UserSchema):
    id: int


class UserLogin(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str


class CompanySchema(BaseModel):
    cnpj: str
    username: str
    email: str
    phone: str
    password: str


class CompanyOut(BaseModel):
    id: int
    cnpj: str
    username: str
    email: str
    phone: str

    class Config:
        orm_mode = True


class CompanyLogin(BaseModel):
    username: str
    password: str


class CursoCreate(BaseModel):
    name: str
    description: str
    youtube_link: str
    company_id: int


class CursoEmpresaOut(BaseModel):
    id: int
    name: str
    description: str
    youtube_link: str

    class Config:
        orm_mode = True