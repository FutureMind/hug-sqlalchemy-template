import hug
from falcon import HTTP_201, HTTP_200
from .serializers import UserRegistrationSerializer, LoginSerializer


@hug.post('/register')
def user_registration(email, password, response):
    serializer = UserRegistrationSerializer(email=email, password=password)
    data = serializer.save()
    response.status = HTTP_201
    return data


@hug.post('/login')
def user_login(login, password, response):
    serializer = LoginSerializer(email=login, password=password)
    data = serializer.login()
    response.status = HTTP_200
    return data
