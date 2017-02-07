from . import APITest, TESTDB_URI
from sqlalchemy_utils import database_exists


class DBTestCase(APITest):

    def test_db_exists(self):
        self.assertTrue(database_exists(TESTDB_URI))
