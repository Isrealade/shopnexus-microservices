from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import os
import redis
from datetime import timedelta
import time
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
# Configure CORS to allow requests from frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize Prometheus metrics with default metrics
metrics = PrometheusMetrics(app, path='/metrics')

# Add default metrics
metrics.info('app_info', 'Application info', version='1.0.0')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@postgres:5432/products')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Initialize Redis client with a default URL for testing
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
redis_client = redis.from_url(redis_url)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    # Make category optional
    category = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category': self.category if hasattr(self, 'category') else None
        }

def init_db():
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            db.create_all()
            print("Database tables created successfully!")
            return
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print("Failed to connect to database after multiple attempts")
                raise e

# Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        print(f"Found {len(products)} products")
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return jsonify([]), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        # Try to get from cache first
        cached_product = redis_client.get(f'product:{product_id}')
        if cached_product:
            return jsonify(eval(cached_product))

        product = Product.query.get_or_404(product_id)
        product_dict = product.to_dict()
        
        # Cache the product
        redis_client.setex(f'product:{product_id}', 3600, str(product_dict))
        
        return jsonify(product_dict)
    except Exception as e:
        print(f"Error fetching product {product_id}: {str(e)}")
        return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['name', 'price', 'stock']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock=data['stock'],
            category=data.get('category', '')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify(product.to_dict()), 201
    except Exception as e:
        print(f"Error creating product: {str(e)}")
        return jsonify({'error': 'Failed to create product'}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        if hasattr(product, 'category'):
            product.category = data.get('category', product.category)
        
        db.session.commit()
        
        # Invalidate cache
        redis_client.delete(f'product:{product_id}')
        
        return jsonify(product.to_dict())
    except Exception as e:
        print(f"Error updating product {product_id}: {str(e)}")
        return jsonify({'error': 'Failed to update product'}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        
        db.session.delete(product)
        db.session.commit()
        
        # Invalidate cache
        redis_client.delete(f'product:{product_id}')
        
        return '', 204
    except Exception as e:
        print(f"Error deleting product {product_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete product'}), 500

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5002, debug=True) 