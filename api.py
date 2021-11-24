import uuid

from fastapi import FastAPI
from pydantic import BaseModel, validator, HttpUrl

app = FastAPI()


class Product(BaseModel):
    id: uuid.UUID = None
    name: str
    price: int

    def __str__(self) -> str:
        return self.name

    @classmethod
    @validator('name')
    def name_length_le_100(cls, v):
        if len(v) > 100:
            raise ValueError('name is longer than 100 characters')
        return v.title()

    @classmethod
    @validator('price')
    def price_positive_integer(cls, v):
        if v < 1:
            raise ValueError('price must be a positive integer')
        return v.title()


class Book(Product):
    weight: int

    @classmethod
    @validator('weight')
    def weight_positive_integer(cls, v):
        if v < 1:
            raise ValueError('weight must be a positive integer')
        return v.title()


class EBook(Product):
    download_link: HttpUrl
