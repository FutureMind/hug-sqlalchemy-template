import hug
from sqlalchemy_utils import database_exists

from . import APITest


class DBTestCase(APITest):

    def test_db_exists(self):
        self.assertTrue(
            database_exists(hug.current_app_config.SQLALCHEMY_DATABASE_URI)
        )
