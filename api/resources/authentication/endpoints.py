import hug
from falcon import HTTP_201
from .serializers import UserRegistrationSerializer
from api.config import db


@hug.post('/register')
def user_registration(email, password, response):
    serializer = UserRegistrationSerializer(email=email, password=password)
    data = serializer.save(db.session)
    response.status = HTTP_201
    return data
