import unittest
from unittest.mock import patch, MagicMock
from app import app, redis_client

class TestProductCache(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('app.redis_client')
    def test_product_caching(self, mock_redis):
        # Mock Redis get to return None (cache miss)
        mock_redis.get.return_value = None
        
        # Mock Redis set to do nothing
        mock_redis.setex = MagicMock()
        
        # Make a request to get a product
        response = self.client.get('/api/products/1')
        
        # Verify Redis was checked
        mock_redis.get.assert_called_once_with('product:1')
        
        # Verify Redis was set with the product data
        mock_redis.setex.assert_called_once()
        
        # Verify the cache key and expiration
        args, kwargs = mock_redis.setex.call_args
        self.assertEqual(args[0], 'product:1')
        self.assertEqual(args[1], 3600)  # 1 hour expiration

    @patch('app.redis_client')
    def test_cache_hit(self, mock_redis):
        # Mock Redis to return cached data
        cached_data = str({
            'id': 1,
            'name': 'Cached Product',
            'description': 'Cached Description',
            'price': 99.99,
            'stock': 10,
            'category': 'Test Category'
        })
        mock_redis.get.return_value = cached_data
        
        # Make a request to get a product
        response = self.client.get('/api/products/1')
        
        # Verify Redis was checked
        mock_redis.get.assert_called_once_with('product:1')
        
        # Verify Redis set was not called (cache hit)
        mock_redis.setex.assert_not_called()

    @patch('app.redis_client')
    def test_cache_invalidation(self, mock_redis):
        # Mock Redis delete
        mock_redis.delete = MagicMock()
        
        # Make a request to update a product
        response = self.client.put('/api/products/1',
            json={
                'name': 'Updated Product',
                'price': 149.99
            },
            headers={'Authorization': 'Bearer test-token'}
        )
        
        # Verify Redis cache was invalidated
        mock_redis.delete.assert_called_once_with('product:1')

if __name__ == '__main__':
    unittest.main() 