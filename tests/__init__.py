import os

import unittest

import hug
from sqlalchemy_utils import database_exists, create_database, drop_database

from alembic import command
from alembic.config import Config

from api.app import create_app, db
from api.models import User
from api.resources.authentication.jwt import jwt_encode


class APITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('TESTING')
        if not database_exists(hug.current_app_config.SQLALCHEMY_DATABASE_URI):
            create_database(hug.current_app_config.SQLALCHEMY_DATABASE_URI)

        alembic_cfg = Config(os.path.join(
            hug.current_app_config.PROJECT_ROOT, 'alembic.ini')
        )
        alembic_cfg.set_main_option(
            'script_location',
            os.path.join(hug.current_app_config.PROJECT_ROOT, 'migrations')
        )
        alembic_cfg.set_main_option(
            'sqlalchemy.url', hug.current_app_config.SQLALCHEMY_DATABASE_URI
        )

        command.upgrade(alembic_cfg, 'head')

    @classmethod
    def tearDownClass(cls):
        drop_database(hug.current_app_config.SQLALCHEMY_DATABASE_URI)


class UserAPITest(APITest):

    @classmethod
    def setUpClass(cls):
        super(UserAPITest, cls).setUpClass()
        db.connect()
        db.session.begin()
        cls.user = User(email='testuser@email.com', password='!Password')
        db.session.add(cls.user)
        db.session.commit()
        cls.user_id = cls.user.id
        cls.user_email = cls.user.email
        db.close()

    def get_authentication_headers(self, user_id, user_email):
        token = jwt_encode(user_id=user_id, user_email=user_email)
        return {'Authorization': token}
