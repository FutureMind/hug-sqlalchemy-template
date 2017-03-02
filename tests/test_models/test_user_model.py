from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError

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
        self.db.session.query(User).delete()
        self.db.session.commit()
        self.db.close()
        super(UserModelTestCase, self).tearDown()

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

    def test_stored_password_is_hashed(self):
        user = User(email='test@email.com', password='TEST')
        self.db.session.add(user)
        self.db.session.commit()
        self.assertNotEqual(user.password, 'TEST')

    def test_password_validation(self):
        user = User(email='test@email.com', password='TEST')
        self.db.session.add(user)
        self.db.session.commit()
        hashed = user.password
        self.assertFalse(user.check_password(hashed))
        self.assertTrue(user.check_password('TEST'))

    def test_email_has_unique_constraint(self):
        user = User(email='test@email.com', password='TEST')
        self.db.session.add(user)
        self.db.session.commit()
        user2 = User(email='test@email.com', password='TEST2')
        self.db.session.add(user2)
        with self.assertRaises(IntegrityError):
            self.db.session.commit()
        self.db.session.rollback()
