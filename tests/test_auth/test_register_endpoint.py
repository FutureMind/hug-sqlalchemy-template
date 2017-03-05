import random
import string

import hug
from falcon import HTTP_201, HTTP_400

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
            body={'email': 'test@email.com', 'password': 'TEST123'}
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
            {'email': 'test@email.com', 'password': 'TEST123'}
        )
        db.connect()
        self.assertEqual(count + 1, db.session.query(User).count())
        user = db.session.query(User).filter_by(email='test@email.com').first()
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.check_password('TEST123'))

    def test_email_validation(self):
        response = hug.test.post(
            app, 'auth/register',
            body={'email': 'not_an_email', 'password': 'TEST123'}
        )
        self.assertEqual(response.status, HTTP_400)
        self.assertIn('errors', response.data)
        self.assertIn('Validation Error', response.data['errors'])
        self.assertEqual(response.data['errors']['Validation Error'],
                         'Invalid email format')

    def test_too_long_data(self):
        random_str = ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(128)
        )
        response = hug.test.post(
            app, 'auth/register',
            body={'email': random_str + '@email.com',
                  'password': 'TEST123'}
        )
        self.assertEqual(response.status, HTTP_400)
        self.assertIn('errors', response.data)
        self.assertIn('Data Error', response.data['errors'])
        self.assertEqual(response.data['errors']['Data Error'],
                         'Cannot save data in database')

    def test_too_short_password_cannot_be_registered(self):
        response = hug.test.post(
            app, 'auth/register',
            {'email': 'test@email.com', 'password': 'T123'}
        )
        self.assertEqual(response.status, HTTP_400)
        self.assertIn('errors', response.data)
        self.assertIn('Validation Error', response.data['errors'])
        self.assertEqual(response.data['errors']['Validation Error'],
                         'Password must be at least 6 character long '
                         'and contain special character')

    def test_too_simple_password_cannot_be_registered(self):
        response = hug.test.post(
            app, 'auth/register',
            {'email': 'test@email.com', 'password': 'testpassword'}
        )
        self.assertEqual(response.status, HTTP_400)
        self.assertIn('errors', response.data)
        self.assertIn('Validation Error', response.data['errors'])
        self.assertEqual(response.data['errors']['Validation Error'],
                         'Password must be at least 6 character long '
                         'and contain special character')
