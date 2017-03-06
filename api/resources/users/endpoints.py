import hug

from api.resources.authentication.jwt import token_auth
from .serializers import UserSerializer


@hug.get('/me', requires=token_auth)
def current_user_detail(user: hug.directives.user):
    serializer = UserSerializer(user=user)
    return serializer.data
