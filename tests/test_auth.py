import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import User
from app.extensions import bcrypt

class TestAuth(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test_secret'
        return app

    def setUp(self):
        db.create_all()

        hashed_password = bcrypt.generate_password_hash("testpassword").decode('utf-8')
        user = User(username="testuser", password=hashed_password)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        response = self.client.post('/register', json={
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered', response.json['message'])

    def test_login(self):
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_invalid(self):
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.json['message'])

if __name__ == '__main__':
    unittest.main()
