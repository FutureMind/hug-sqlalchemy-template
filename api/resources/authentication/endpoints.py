import hug
from falcon import HTTP_201
from api.models import User
from api.config import db


@hug.post('/register')
def user_registration(email, password, response):
    user = User(email=email, password=password)
    db.session.begin()
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    response.status = HTTP_201
    return {'email': user.email, 'id': user.id}
