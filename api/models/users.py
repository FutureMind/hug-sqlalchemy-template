import bcrypt
from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password, self.password)
