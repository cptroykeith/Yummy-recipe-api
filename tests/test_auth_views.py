import unittest
import json
from app import create_app, db


class TestRecipeApp(unittest.TestCase):
    """class to test valid user registration and login."""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'email': 'angelalehru@gmail.com',
                     'username': 'Gela',
                     'password': 'forgetfulangela',
                     'confirm_password': 'forgetfulangela'}
        
        self.user_login = {'email': 'angelalehru@gmail.com',
                           'password': 'forgetfulangela'}

        with self.app.app_context():
            db.create_all()

    def test_register(self):
        """Test API can register users (POST request)"""
        res = self.client().post('/api-v1/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)

    def test_login(self):
        """Test API can login users (POST request)"""
        self.test_register()
        res = self.client().post('/api-v1/auth/login', data=self.user_login)
        self.assertEqual(res.status_code, 200)
    
    def test_logout(self):
        """Test API can logout users (POST request)"""
        self.test_register()
        result=self.client().post('/api-v1/auth/login', data=self.user_login)
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api-v1/auth/logout',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()