from ..core.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    fields = ('email', 'location', 'about', 'name')

    def __init__(self, user):
        self.user = user

    @property
    def data(self):
        return self.to_dict(self.user)
