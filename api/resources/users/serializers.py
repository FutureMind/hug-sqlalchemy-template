from ..core.serializers import ModelSerializer
from api.models import User
from api.app import db


class UserBaseSerializer(ModelSerializer):

    fields = ('email', 'location', 'about', 'name')


class UserSerializer(UserBaseSerializer):

    def __init__(self, user):
        self.user = user

    @property
    def data(self):
        return self.to_dict(self.user)


class UserListSerializer(UserBaseSerializer):

    @property
    def data(self):
        return self.to_list(db.session.query(User).all())
