import unittest
from app import app, db, User
from unittest.mock import patch, MagicMock
import json

class TestUserService(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        # Mock Redis
        self.redis_patcher = patch('app.redis_client')
        self.mock_redis = self.redis_patcher.start()
        self.mock_redis.get.return_value = None
        self.mock_redis.setex = MagicMock()
        self.mock_redis.delete = MagicMock()
        
        with app.app_context():
            db.create_all()
            
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.redis_patcher.stop()
        
    def test_register_user(self):
        response = self.client.post('/api/users/register',
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass'
            })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User created successfully')
        
    def test_register_duplicate_username(self):
        # First registration
        self.client.post('/api/users/register',
            json={
                'username': 'testuser',
                'email': 'test1@example.com',
                'password': 'testpass'
            })
        
        # Try to register same username again
        response = self.client.post('/api/users/register',
            json={
                'username': 'testuser',
                'email': 'test2@example.com',
                'password': 'testpass'
            })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username already exists')
        
    def test_login(self):
        # Register a user first
        self.client.post('/api/users/register',
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass'
            })
        
        # Try to login
        response = self.client.post('/api/users/login',
            json={
                'username': 'testuser',
                'password': 'testpass'
            })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        
    def test_login_invalid_credentials(self):
        response = self.client.post('/api/users/login',
            json={
                'username': 'testuser',
                'password': 'wrongpass'
            })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid credentials')
        
    def test_get_profile(self):
        # Register and login
        self.client.post('/api/users/register',
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass'
            })
        login_response = self.client.post('/api/users/login',
            json={
                'username': 'testuser',
                'password': 'testpass'
            })
        token = json.loads(login_response.data)['access_token']
        
        # Get profile with proper Authorization header
        response = self.client.get('/api/users/profile',
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json')
        if response.status_code != 200:
            print('DEBUG RESPONSE:', response.status_code, response.data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        
    def test_get_profile_unauthorized(self):
        response = self.client.get('/api/users/profile')
        self.assertEqual(response.status_code, 401)
        
if __name__ == '__main__':
    unittest.main() 