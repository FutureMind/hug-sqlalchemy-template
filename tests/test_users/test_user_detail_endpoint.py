import hug
from falcon import HTTP_200

from .. import UserAPITest
from api.config import db
from api.app import app


class LoggedUserDetailEndpointTestCase(UserAPITest):

    def test_response(self):
        headers = self.get_authenticate_headers(user_id=self.user_id,
                                                user_email=self.user_email)
        response = hug.test.get(app, 'users/me', headers=headers)
        self.assertEqual(response.status, HTTP_200)
        self.assertIn('email', response.data)
        self.assertIn('name', response.data)
        self.assertIn('location', response.data)
        self.assertIn('about', response.data)
        self.assertEqual(response.data['email'], 'testuser@email.com')
        self.assertEqual(response.data['name'], '')
        self.assertEqual(response.data['location'], '')
        self.assertEqual(response.data['about'], '')

    def test_response_after_user_update_data(self):
        headers = self.get_authenticate_headers(user_id=self.user_id,
                                                user_email=self.user_email)
        db.connect()
        self.user.about = 'Western wind chases foamed waves'
        self.user.name = 'Abbot'
        self.user.location = 'Sigil'
        db.session.add(self.user)
        db.close()
        response = hug.test.get(app, 'users/me', headers=headers)
        self.assertEqual(response.data['name'], 'Abbot')
        self.assertEqual(response.data['location'], 'Sigil')
        self.assertEqual(response.data['about'],
                         'Western wind chases foamed waves')
