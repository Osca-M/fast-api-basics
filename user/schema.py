import uuid

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
