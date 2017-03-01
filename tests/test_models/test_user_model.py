from sqlalchemy.sql import exists

from .. import APITest, TESTDB_URI
from api.models.users import User
from api.db import SQLAlchemy
from api.app import app


class UserModelTestCase(APITest):

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.db = SQLAlchemy()
        self.db.init_app(app, TESTDB_URI)
        self.db.connect()

    def tearDown(self):
        self.db.close()
        super(UserModelTestCase)

    def test_saving_and_retrieving_user(self):
        count = self.db.session.query(User).count()
        user = User(email='test@email.com', password='TEST')
        self.db.session.add(user)
        self.assertIsNone(user.id)
        self.db.session.commit()
        self.assertEqual(count + 1, self.db.session.query(User).count())
        self.assertIsNotNone(user.id)
        self.assertTrue(
            self.db.session.query(
                exists().where(User.email == 'test@email.com')
            ).scalar()
        )
