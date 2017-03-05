import datetime

import jwt
from falcon import HTTPError, HTTP_401

from api.config import config


def jwt_encode(user_id, user_email):
    expires = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=config.JWT_EXPIRATION_TIME)
    payload = {
        'exp': expires,
        'id': user_id,
        'email': user_email
    }
    return jwt.encode(payload, config.SECRET_KEY)


def jwt_decode(token):
    try:
        decoded = jwt.decode(token, config.SECRET_KEY)
    except jwt.DecodeError:
        raise HTTPError(status=HTTP_401, title='Authentication Error',
                        description='Invalid token')
    except jwt.ExpiredSignatureError:
        raise HTTPError(status=HTTP_401, title='Authentication Error',
                        description='Token expired')
    else:
        return decoded
