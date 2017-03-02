import hug

from api.config import db, config

from api.resources.authentication import endpoints as auth_endpoints


app = hug.API(__name__)

# init DB
db.init_app(app, config.SQLALCHEMY_DATABASE_URI)

app.extend(auth_endpoints, '/auth')
