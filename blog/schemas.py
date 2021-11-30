from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    published: bool


class User(BaseModel):
    name: str
    email: str
    password: str
