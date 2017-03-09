import os


# Declare your config classes with settings variables here
class Config:
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SECRET_KEY = os.environ['SECRET_KEY']
    JWT_EXPIRATION_TIME = 60 * 60 * 24 * 14  # 2 weeks


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_SQLALCHEMY_DATABASE_URI',
        DevelopmentConfig.SQLALCHEMY_DATABASE_URI + '_test'
    )
    JWT_EXPIRATION_TIME = 2  # 2 seconds


class ProductionConfig(Config):
    pass


config_dict = {
    'DEVELOPMENT': DevelopmentConfig,
    'PRODUCTION': ProductionConfig,
    'TESTING': TestingConfig,

    'default': DevelopmentConfig
}
