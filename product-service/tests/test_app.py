import unittest
import json
from unittest.mock import patch, MagicMock
from app import app, db, Product, create_access_token
import os

class TestProductService(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            # Mock Redis client
            self.redis_patcher = patch('app.redis_client')
            self.mock_redis = self.redis_patcher.start()
            self.mock_redis.get.return_value = None
            self.mock_redis.setex = MagicMock()
            self.mock_redis.delete = MagicMock()
            # Create test token
            self.test_token = create_access_token(identity='test-user')

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.redis_patcher.stop()

    def test_create_product(self):
        response = self.client.post('/api/products',
            json={
                'name': 'Test Product',
                'description': 'Test Description',
                'price': 99.99,
                'stock': 10,
                'category': 'Test Category'
            },
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(data['price'], 99.99)

    def test_get_products(self):
        # Create a product first
        self.client.post('/api/products',
            json={
                'name': 'Test Product',
                'description': 'Test Description',
                'price': 99.99,
                'stock': 10,
                'category': 'Test Category'
            },
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        
        # Get all products
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Product')

    def test_get_product(self):
        # Create a product first
        create_response = self.client.post('/api/products',
            json={
                'name': 'Test Product',
                'description': 'Test Description',
                'price': 99.99,
                'stock': 10,
                'category': 'Test Category'
            },
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        product_id = json.loads(create_response.data)['id']
        
        # Get the specific product
        response = self.client.get(f'/api/products/{product_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(data['price'], 99.99)

    def test_update_product(self):
        # Create a product first
        create_response = self.client.post('/api/products',
            json={
                'name': 'Test Product',
                'description': 'Test Description',
                'price': 99.99,
                'stock': 10,
                'category': 'Test Category'
            },
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        product_id = json.loads(create_response.data)['id']
        
        # Update the product
        response = self.client.put(f'/api/products/{product_id}',
            json={
                'name': 'Updated Product',
                'price': 149.99
            },
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Product')
        self.assertEqual(data['price'], 149.99)

    def test_delete_product(self):
        # Create a product first
        create_response = self.client.post('/api/products',
            json={
                'name': 'Test Product',
                'description': 'Test Description',
                'price': 99.99,
                'stock': 10,
                'category': 'Test Category'
            },
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        product_id = json.loads(create_response.data)['id']
        
        # Delete the product
        response = self.client.delete(f'/api/products/{product_id}',
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 204)
        
        # Verify product is deleted
        get_response = self.client.get(f'/api/products/{product_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 