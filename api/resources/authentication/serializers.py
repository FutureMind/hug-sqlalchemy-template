import re

from falcon.errors import HTTPError
from falcon import HTTP_400

from api.config import db
from api.models import User
from ..core.serializers import BaseSerializer
from .jwt import jwt_encode


class AuthBaseSerializer(BaseSerializer):

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def _validate_email(self):
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        self.email):
            raise HTTPError(status=HTTP_400, title='Validation Error',
                            description='Invalid email format')


class UserRegistrationSerializer(AuthBaseSerializer):

    def to_dict(self, user):
        return {
            'id': user.id,
            'email': user.email
        }

    def _save_user(self, user):
        db.session.begin()
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise HTTPError(status=HTTP_400, title='Data Error',
                            description='Cannot save data in database')

    def _validate_password(self):
        if len(self.password) < 6 or self.password.isalpha():
            raise HTTPError(
                status=HTTP_400, title='Validation Error',
                description='Password must be at least 6 character long '
                            'and contain special character'
            )

    def save(self):
        self.validate()
        user = User(email=self.email, password=self.password)
        self._save_user(user)
        return self.to_dict(user)


class LoginSerializer(AuthBaseSerializer):

    def _get_object(self):
        user = db.session.query(User).filter_by(email=self.email).first()
        if not user:
            raise HTTPError(status=HTTP_400, title='Validation Error',
                            description='Invalid credentials')
        return user

    def _authenticate(self, user):
        if not user.check_password(self.password):
            raise HTTPError(status=HTTP_400, title='Validation Error',
                            description='Invalid credentials')

    def login(self):
        self.validate()
        user = self._get_object()
        self._authenticate(user)
        token = jwt_encode(user_id=user.id, user_email=user.email)
        return {'Token': token}
