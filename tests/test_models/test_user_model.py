from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError

from .. import APITest
from api.models.users import User
from api.config import db


class UserModelTestCase(APITest):

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        db.connect()
        db.session.begin()

    def tearDown(self):
        db.session.begin()
        db.session.query(User).delete()
        db.session.commit()
        db.close()
        super(UserModelTestCase, self).tearDown()

    def test_saving_and_retrieving_user(self):
        count = db.session.query(User).count()
        user = User(email='test@email.com', password='TEST')
        db.session.add(user)
        self.assertIsNone(user.id)
        db.session.commit()
        self.assertEqual(count + 1, db.session.query(User).count())
        self.assertIsNotNone(user.id)
        self.assertTrue(
            db.session.query(
                exists().where(User.email == 'test@email.com')
            ).scalar()
        )

    def test_stored_password_is_hashed(self):
        user = User(email='test@email.com', password='TEST')
        db.session.add(user)
        db.session.commit()
        self.assertNotEqual(user.password, 'TEST')

    def test_password_validation(self):
        user = User(email='test@email.com', password='TEST')
        db.session.add(user)
        db.session.commit()
        hashed = user.password
        self.assertFalse(user.check_password(hashed))
        self.assertTrue(user.check_password('TEST'))

    def test_email_has_unique_constraint(self):
        user = User(email='test@email.com', password='TEST')
        db.session.add(user)
        user2 = User(email='test@email.com', password='TEST2')
        db.session.add(user2)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()
