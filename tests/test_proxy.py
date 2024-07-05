import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import User
from app.extensions import bcrypt

class TestProxy(TestCase):

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

    def get_access_token(self):
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        return response.json['access_token']

    def test_nodes(self):
        
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        
        response = self.client.get('/nodes?view=summary', headers=headers)
        print("response: ", response.json)
        self.assertEqual(response.status_code, 200)
        print(response.json)
        self.assertIn('result', response.json)


if __name__ == '__main__':
    unittest.main()
