from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    name: str
    email: str
    password: str
    role: str
    agree_terms: bool = True


class LoginSchema(BaseModel):
    email: str
    password: str


class LoginResultSchema(BaseModel):
    username: str
    name: str
    email: str
    role: str