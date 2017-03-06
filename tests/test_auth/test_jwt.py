import time

from falcon.errors import HTTPError
from falcon import HTTP_401
import hug

from .. import UserAPITest
from api.app import app
from api.config import db
from api.resources.authentication.jwt import (jwt_encode, jwt_decode,
                                              verify_user)


class JWTEncodingTestCase(UserAPITest):

    def test_jwt_encoding_and_decoding(self):
        encoded = jwt_encode(user_email=self.user_email, user_id=self.user_id)
        decoded = jwt_decode(encoded)
        self.assertIn('id', decoded)
        self.assertIn('email', decoded)
        self.assertEqual(decoded['id'], self.user.id)
        self.assertEqual(decoded['email'], self.user.email)

    def test_jwt_decoding_bad_token(self):
        invalid = 'Token.Token.Token'
        with self.assertRaises(HTTPError):
            jwt_decode(invalid)

    def test_jwt_token_expiration(self):
        encoded = jwt_encode(user_email=self.user_email, user_id=self.user_id)
        time.sleep(3)
        with self.assertRaises(HTTPError):
            jwt_decode(encoded)


class UserVerifyTestCase(UserAPITest):

    def test_verify_existing_user(self):
        token = jwt_encode(user_email=self.user_email, user_id=self.user_id)
        user = verify_user(token)
        db.connect()
        self.assertEqual(user.id, self.user_id)
        self.assertEqual(user.email, self.user_email)
        db.close()

    def test_verify_user_from_bad_token(self):
        token = 'Token.Token.Token'
        db.connect()
        with self.assertRaises(HTTPError):
            verify_user(token)
        db.close()

    def test_verify_token_from_not_existing_user(self):
        token = jwt_encode(user_email='not_existing@email.com', user_id=1)
        db.connect()
        with self.assertRaises(HTTPError):
            verify_user(token)
        db.close()


class AuthenticationRequiredViewsTestCase(UserAPITest):

    def test_no_token_provided(self):
        response = hug.test.get(app, 'users/me')
        self.assertEqual(response.status, HTTP_401)
        self.assertIn('Authentication Required', response.data['errors'])

    def test_not_existing_user_data(self):
        headers = self.get_authenticate_headers(
            user_email='not_existing@email.com', user_id=4
        )
        response = hug.test.get(app, 'users/me', headers=headers)
        self.assertEqual(response.status, HTTP_401)
        self.assertIn('Authentication Error', response.data['errors'])
        self.assertEqual(response.data['errors']['Authentication Error'],
                         'Invalid token')

    def test_changing_email_invalidates_token(self):
        db.connect()
        self.user.email = 'another@email.com'
        db.session.add(self.user)
        db.close()
        headers = self.get_authenticate_headers(
            user_email=self.user_email, user_id=self.user_id
        )
        response = hug.test.get(app, 'users/me', headers=headers)
        self.assertEqual(response.status, HTTP_401)
        self.assertIn('Authentication Error', response.data['errors'])
        self.assertEqual(response.data['errors']['Authentication Error'],
                         'Invalid token')
        # change email back
        db.connect()
        self.user.email = self.user_email
        db.session.add(self.user)
        db.session.close()
