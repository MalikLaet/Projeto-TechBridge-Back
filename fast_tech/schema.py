from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    username: str
    email: EmailStr
    telefone: str
    password: str


from pydantic import BaseModel


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    telefone: str

    class Config:
        orm_mode = True


class UserDB(UserSchema):
    id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str
