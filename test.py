import unittest
from flask import Flask, session
from app import db
from app.models import User
from app.users.views import users

class UsersTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'secret'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        user_data = {'first_name': 'John', 'last_name': 'Doe',
                     'email': 'roy@example.com', 'password': 'secret'}
        response = self.client.post('/api/signup', json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Successfully signed up'})
        user = User.query.filter_by(email='roy@example.com').first()
        self.assertIsNotNone(user)

    def test_login(self):
        user_data = {'first_name': 'John', 'last_name': 'Doe',
                     'email': 'roy@example.com', 'password': 'secret'}
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/login', json={'email': 'roy@example.com', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})
        self.assertTrue(session.get('logged_in'))

        response = self.client.post('/api/login', json={'email': 'roy@example.com', 'password': 'incorrect'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': False})

    def test_logout(self):
        with self.client:
            self.client.post('/api/logout')
            self.assertFalse(session.get('logged_in'))

if __name__ == '__main__':
    unittest.main()