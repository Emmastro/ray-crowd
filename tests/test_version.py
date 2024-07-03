import unittest
from flask_testing import TestCase
from app import create_app

class TestVersion(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def test_version(self):
        response = self.client.get('/api/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['version'], '1.0.0')
        self.assertEqual(response.json['description'], 'Crowd Computing Platform API')

if __name__ == '__main__':
    unittest.main()
