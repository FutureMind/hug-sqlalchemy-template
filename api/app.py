import hug

from api.config import db, config


app = hug.API(__name__)

# init DB
db.init_app(app, config.SQLALCHEMY_DATABASE_URI)
