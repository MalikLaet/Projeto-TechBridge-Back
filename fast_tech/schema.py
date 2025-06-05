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
