import os

from api.db import SQLAlchemy


# Declare your config classes with settings variables here
class Config:
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SECRET_KEY = os.environ['SECRET_KEY']
    JWT_EXPIRATION_TIME = 60 * 60 * 24 * 14  # 2 weeks


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    TEST_SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI + '_test'
    )
    JWT_EXPIRATION_TIME = 2  # 2 seconds


class ProductionConfig(Config):
    pass


ENV_MAPPING = {
    'DEVELOPMENT': DevelopmentConfig,
    'PRODUCTION': ProductionConfig,
}

# Globals. If you like move it to separate module
db = SQLAlchemy(autocommit=True)
config = ENV_MAPPING[os.environ.get('API_ENV', 'DEVELOPMENT')]
