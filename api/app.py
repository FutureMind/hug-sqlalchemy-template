import os
import hug

from api.config import config_dict
from api.db import SQLAlchemy


db = SQLAlchemy(autocommit=True)


def create_app(config_name):
    config = config_dict[config_name]
    app = hug.API(__name__)
    hug.current_app_config = config

    db.init_app(app, config.SQLALCHEMY_DATABASE_URI)

    from api.resources.authentication import endpoints as auth_endpoints
    app.extend(auth_endpoints, '/auth')
    from api.resources.users import endpoints as user_endpoints
    app.extend(user_endpoints, '/users')

    hug.current_app = app

    return app


app = create_app(os.getenv('APP_CONFIG') or 'default')
