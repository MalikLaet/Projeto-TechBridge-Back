from pydantic import BaseModel, EmailStr


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
    email: EmailStr
    password: str
