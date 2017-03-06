import bcrypt
from sqlalchemy import Column, Integer, String, Text

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    name = Column(String(100), nullable=False)
    about = Column(Text(), nullable=False)
    location = Column(String(60), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = self.set_password(password)
        self.location = ''
        self.name = ''
        self.about = ''

    def set_password(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password, self.password)
