import hug
from falcon import HTTP_200

from sqlalchemy import not_

from api.app import app
from api.config import db
from api.models import User
from .. import UserAPITest


class UserListEndpointTestCase(UserAPITest):

    def setUp(self):
        super(UserListEndpointTestCase, self).setUp()
        self.headers = self.get_authentication_headers(
            user_id=self.user_id, user_email=self.user_email
        )

    def tearDown(self):
        # delete all users except base user
        db.connect()
        db.session.query(User).filter(
            not_(User.email == 'testuser@email.com')
        ).delete()
        db.close()
        super(UserListEndpointTestCase, self).tearDown()

    def test_one_user_response(self):
        response = hug.test.get(app, 'users', headers=self.headers)
        self.assertEqual(response.status, HTTP_200)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), 1)
        user = response.data[0]
        self.assertEqual(user['email'], 'testuser@email.com')
        self.assertEqual(user['name'], '')
        self.assertEqual(user['location'], '')
        self.assertEqual(user['about'], '')

    def test_many_users_response(self):
        # create additional users
        db.connect()
        db.session.begin()
        user2 = User(email='seconduser@email.com', password='!secondPassword')
        user2.about = 'I am second user'
        user3 = User(email='thirduser@email.com', password='!thirdPassword')
        user3.location = 'Third location'
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        db.close()
        # check response
        response = hug.test.get(app, 'users', headers=self.headers)
        self.assertEqual(response.status, HTTP_200)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['email'], 'testuser@email.com')
        self.assertEqual(response.data[1]['email'], 'seconduser@email.com')
        self.assertEqual(response.data[2]['email'], 'thirduser@email.com')
        self.assertEqual(response.data[1]['about'], 'I am second user')
        self.assertEqual(response.data[2]['location'], 'Third location')
