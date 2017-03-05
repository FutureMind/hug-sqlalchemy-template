import time

from falcon.errors import HTTPError

from .. import APITest
from api.config import db
from api.models import User
from api.resources.authentication.jwt import jwt_encode, jwt_decode


class JWTEncodingTestCase(APITest):

    @classmethod
    def setUpClass(cls):
        super(JWTEncodingTestCase, cls).setUpClass()
        db.connect()
        db.session.begin()
        cls.user = User(email='testuser@email.com', password='!Password')
        db.session.add(cls.user)
        db.session.commit()
        cls.user_id = cls.user.id
        cls.user_email = cls.user.email
        db.close()

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
