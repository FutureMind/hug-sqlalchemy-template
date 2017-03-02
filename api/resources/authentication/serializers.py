import re

from api.models import User


class UserRegistrationSerializer:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def _validate_email(self):
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        self.email)

    def validate(self):
        return self._validate_email()

    def to_dict(self, user):
        return {
            'id': user.id,
            'email': user.email
        }

    def save(self, db_session):
        if self.validate():
            user = User(email=self.email, password=self.password)
            db_session.add(user)
            db_session.commit()
            return self.to_dict(user)
