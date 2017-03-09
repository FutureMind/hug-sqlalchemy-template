import datetime

import jwt
from falcon import HTTPError, HTTP_401
import hug

from api.app import db
from api.models import User


def jwt_encode(user_id, user_email):
    expires = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=hug.current_app_config.JWT_EXPIRATION_TIME)
    payload = {
        'exp': expires,
        'id': user_id,
        'email': user_email
    }
    return jwt.encode(payload, hug.current_app_config.SECRET_KEY)


def jwt_decode(token):
    try:
        decoded = jwt.decode(token, hug.current_app_config.SECRET_KEY)
    except jwt.DecodeError:
        raise HTTPError(status=HTTP_401, title='Authentication Error',
                        description='Invalid token')
    except jwt.ExpiredSignatureError:
        raise HTTPError(status=HTTP_401, title='Authentication Error',
                        description='Token expired')
    else:
        return decoded


def verify_user(token):
    decoded = jwt_decode(token)
    user = db.session.query(User).filter_by(email=decoded['email']).first()
    if not user:
        raise HTTPError(status=HTTP_401, title='Authentication Error',
                        description='Invalid token')
    return user


token_auth = hug.authentication.token(verify_user=verify_user)
