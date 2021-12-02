from typing import Union

from passlib.context import CryptContext


class Password:
    def __init__(self, password: str, hashed_password=None):
        self.password = password
        self.hashed_password = hashed_password
        self.cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def encrypt(self) -> str:
        return self.cxt.hash(self.password)

    def verify(self) -> bool:
        return self.cxt.verify(self.password, self.hashed_password)
