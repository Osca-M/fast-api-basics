from passlib.context import CryptContext


class Password:
    def __init__(self, password: str):
        self.password = password
        self.cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def encrypt(self):
        return self.cxt.hash(self.password)
