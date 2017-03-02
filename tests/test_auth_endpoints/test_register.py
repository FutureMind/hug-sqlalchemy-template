import hug
from falcon import HTTP_201

from .. import APITest
from api.app import app
from api.config import db
from api.models import User


class RegistrationEndpointTestCase(APITest):

    def tearDown(self):
        db.connect()
        db.session.query(User).delete()
        db.close()
        super(RegistrationEndpointTestCase, self).tearDown()

    def test_user_registration_response(self):
        response = hug.test.post(
            app, 'auth/register',
            body={'email': 'test@email.com', 'password': 'TEST'}
        )
        self.assertEqual(response.status, HTTP_201)
        self.assertIn('email', response.data)
        self.assertIn('id', response.data)
        self.assertTrue(isinstance(response.data['id'], int))
        self.assertEqual(response.data['email'], 'test@email.com')

    def test_user_is_properly_saved_after_registration(self):
        db.connect()
        count = db.session.query(User).count()
        db.close()
        hug.test.post(
            app, 'auth/register',
            {'email': 'test@email.com', 'password': 'TEST'}
        )
        db.connect()
        self.assertEqual(count + 1, db.session.query(User).count())
        user = db.session.query(User).filter_by(email='test@email.com').first()
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.check_password('TEST'))
