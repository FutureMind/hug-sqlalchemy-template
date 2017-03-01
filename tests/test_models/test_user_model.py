from sqlalchemy.sql import exists

from .. import APITest
from api.models.users import User
from api.config import db


class UserModelTestCase(APITest):

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        db.connect()

    def tearDown(self):
        db.close()
        super(UserModelTestCase)

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
