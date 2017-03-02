import re

from falcon.errors import HTTPError
from falcon import HTTP_400

from api.models import User


class UserRegistrationSerializer:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def _validate_email(self):
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        self.email)

    def validate(self):
        if not self._validate_email():
            raise HTTPError(status=HTTP_400, title='Validation Error',
                            description='Invalid email format')

    def to_dict(self, user):
        return {
            'id': user.id,
            'email': user.email
        }

    def _save_user(self, user, db_session):
        db_session.begin()
        try:
            db_session.add(user)
            db_session.commit()
        except:
            db_session.rollback()
            raise HTTPError(status=HTTP_400, title='Data Error',
                            description='Cannot save data in database')

    def save(self, db_session):
        self.validate()
        user = User(email=self.email, password=self.password)
        self._save_user(user, db_session)
        return self.to_dict(user)
