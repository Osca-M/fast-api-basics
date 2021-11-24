import uuid
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, validator

app = FastAPI()


# noinspection PyMethodParameters
class Product(BaseModel):
    id: Optional[uuid.UUID]
    name: str
    price: int

    def __str__(self) -> str:
        return self.name

    @validator('name')
    def name_length_le_100(cls, v):
        if len(v) > 100:
            raise ValueError('name is longer than 100 characters')
        return v

    @validator('price')
    def price_positive_integer(cls, v):
        if v < 1:
            raise ValueError('price must be a positive integer')
        return v


# noinspection PyMethodParameters
class Book(Product):
    weight: int

    @validator('weight')
    def weight_positive_integer(cls, v):
        if v < 1:
            raise ValueError('weight must be a positive integer')
        return v


books = {}


# create Book
@app.post(path='/add-book')
def create_book(book: Book):
    pk = uuid.uuid4()
    if pk in list(books.keys()):
        pk = uuid.uuid4()
    book.id = pk
    books[pk] = book
    return {'detail': 'Book added successfully'}


# List all books
@app.get(path='/get-books')
def list_books():
    return books


# Book detail
@app.get(path='/get-book/{pk}')
def get_ebook(pk: uuid.UUID):
    return books.get(pk, {})

