import uuid
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    id: uuid.UUID
    name: str
    email: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
