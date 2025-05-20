import requests
import random
import time
import threading
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Service URLs
USER_SERVICE_URL = "http://user-service:5001/api/users"  # Updated to match actual endpoint
PRODUCT_SERVICE_URL = "http://product-service:5002/api/products"  # Updated to match actual endpoint

# Load configuration
MAX_USERS = 100  # Maximum number of concurrent users at 100% load
LOAD_PERCENTAGE = int(os.getenv('LOAD_PERCENTAGE', '50'))  # Default to 50% load
ERROR_PERCENTAGE = int(os.getenv('ERROR_PERCENTAGE', '2'))  # Default to 2% error rate

# Calculate actual values
NUM_USERS = int((MAX_USERS * LOAD_PERCENTAGE) / 100)
ERROR_RATE = ERROR_PERCENTAGE / 100  # Convert percentage to decimal

# Sample data
SAMPLE_USERS = [
    {"username": f"user{i}", "email": f"user{i}@example.com", "password": "password123"}
    for i in range(1, 101)  # Increased to 100 users
]

SAMPLE_PRODUCTS = [
    {
        "name": f"Product {i}",
        "description": f"Description for product {i}",
        "price": round(random.uniform(10.0, 1000.0), 2),
        "stock": random.randint(0, 100),
        "category": random.choice(["Electronics", "Clothing", "Books", "Home", "Sports", "Toys"])
    }
    for i in range(1, 51)  # Increased to 50 products
]

class UserSession:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.token: Optional[str] = None
        self.registered_products: List[Dict] = []
        self.session_start = datetime.now()
        self.actions_completed = 0

    def register_user(self) -> bool:
        try:
            user_data = SAMPLE_USERS[self.user_id]
            response = requests.post(f"{USER_SERVICE_URL}/register", json=user_data)
            if response.status_code == 201:
                logger.info(f"User {self.user_id} registered successfully")
                return True
            else:
                logger.error(f"Failed to register user {self.user_id}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error registering user {self.user_id}: {e}")
            return False

    def login(self) -> bool:
        try:
            user_data = SAMPLE_USERS[self.user_id]
            response = requests.post(
                f"{USER_SERVICE_URL}/login",
                json={"username": user_data['username'], "password": user_data['password']}
            )
            if response.status_code == 200:
                self.token = response.json().get('access_token')
                logger.info(f"User {self.user_id} logged in successfully")
                return True
            else:
                logger.error(f"Failed to login user {self.user_id}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error logging in user {self.user_id}: {e}")
            return False

    def get_profile(self) -> bool:
        if not self.token:
            return False
        try:
            response = requests.get(
                f"{USER_SERVICE_URL}/profile",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                logger.info(f"User {self.user_id} retrieved profile successfully")
                return True
            else:
                logger.error(f"Failed to get profile for user {self.user_id}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error getting profile for user {self.user_id}: {e}")
            return False

    def browse_products(self) -> Optional[List[Dict]]:
        try:
            response = requests.get(f"{PRODUCT_SERVICE_URL}")
            if response.status_code == 200:
                logger.info(f"User {self.user_id} browsed products successfully")
                return response.json()
            else:
                logger.error(f"Failed to browse products for user {self.user_id}: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error browsing products for user {self.user_id}: {e}")
            return None

    def create_product(self) -> bool:
        if not self.token:
            return False
        try:
            product_data = random.choice(SAMPLE_PRODUCTS)
            response = requests.post(
                f"{PRODUCT_SERVICE_URL}",
                headers={"Authorization": f"Bearer {self.token}"},
                json=product_data
            )
            if response.status_code == 201:
                self.registered_products.append(response.json())
                logger.info(f"User {self.user_id} created product successfully")
                return True
            else:
                logger.error(f"Failed to create product for user {self.user_id}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error creating product for user {self.user_id}: {e}")
            return False

    def update_product(self) -> bool:
        if not self.token or not self.registered_products:
            return False
        try:
            product = random.choice(self.registered_products)
            update_data = {
                "name": f"Updated {product['name']}",
                "price": round(random.uniform(10.0, 1000.0), 2),
                "stock": random.randint(0, 100),
                "description": f"Updated description for product {product['id']}"
            }
            response = requests.put(
                f"{PRODUCT_SERVICE_URL}/{product['id']}",
                headers={"Authorization": f"Bearer {self.token}"},
                json=update_data
            )
            if response.status_code == 200:
                logger.info(f"User {self.user_id} updated product successfully")
                return True
            else:
                logger.error(f"Failed to update product for user {self.user_id}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error updating product for user {self.user_id}: {e}")
            return False

    def delete_product(self) -> bool:
        if not self.token or not self.registered_products:
            return False
        try:
            product = random.choice(self.registered_products)
            response = requests.delete(
                f"{PRODUCT_SERVICE_URL}/{product['id']}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 204:
                self.registered_products.remove(product)
                logger.info(f"User {self.user_id} deleted product successfully")
                return True
            else:
                logger.error(f"Failed to delete product for user {self.user_id}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error deleting product for user {self.user_id}: {e}")
            return False

def simulate_error() -> bool:
    """Simulate random errors based on different scenarios and configured error rate"""
    # Only simulate errors if random number is below the error rate
    if random.random() > ERROR_RATE:
        return False
        
    error_scenarios = [
        (0.4, "rate_limit"),      # 40% of errors are rate limits
        (0.3, "invalid_data"),    # 30% of errors are invalid data
        (0.2, "server_error"),    # 20% of errors are server errors
        (0.1, "timeout")          # 10% of errors are timeouts
    ]
    
    for probability, error_type in error_scenarios:
        if random.random() < probability:
            if error_type == "rate_limit":
                time.sleep(0.1)  # Simulate rate limiting
                return True
            elif error_type == "invalid_data":
                return True
            elif error_type == "server_error":
                time.sleep(0.2)  # Simulate server processing
                return True
            elif error_type == "timeout":
                time.sleep(2)  # Simulate timeout
                return True
    return False

def register_user(user_id: int) -> Dict[str, Any]:
    """Register a new user with error simulation"""
    if simulate_error():
        logging.error(f"User {user_id}: Simulated error during registration")
        return None
        
    user_data = {
        "username": f"user{user_id}",
        "email": f"user{user_id}@example.com",
        "password": f"password{user_id}"
    }
    
    try:
        response = requests.post(f"{USER_SERVICE_URL}/register", json=user_data)
        if response.status_code == 201:
            logging.info(f"User {user_id}: Registration successful")
            return response.json()
        else:
            logging.error(f"User {user_id}: Registration failed with status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"User {user_id}: Registration error - {str(e)}")
        return None

def login_user(user_id: int) -> str:
    """Login user with error simulation"""
    if simulate_error():
        logging.error(f"User {user_id}: Simulated error during login")
        return None
        
    login_data = {
        "username": f"user{user_id}",
        "password": f"password{user_id}"
    }
    
    try:
        response = requests.post(f"{USER_SERVICE_URL}/login", json=login_data)
        if response.status_code == 200:
            logging.info(f"User {user_id}: Login successful")
            return response.json().get("access_token")
        else:
            logging.error(f"User {user_id}: Login failed with status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"User {user_id}: Login error - {str(e)}")
        return None

def get_user_profile(user_id: int, token: str) -> Dict[str, Any]:
    """Get user profile with error simulation"""
    if simulate_error():
        logging.error(f"User {user_id}: Simulated error during profile retrieval")
        return None
        
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{USER_SERVICE_URL}/profile", headers=headers)
        if response.status_code == 200:
            logging.info(f"User {user_id}: Profile retrieved successfully")
            return response.json()
        else:
            logging.error(f"User {user_id}: Profile retrieval failed with status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"User {user_id}: Profile retrieval error - {str(e)}")
        return None

def get_products(token: str) -> list:
    """Get products with error simulation"""
    if simulate_error():
        logging.error("Simulated error during product listing")
        return []
        
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}", headers=headers)
        if response.status_code == 200:
            logging.info("Products retrieved successfully")
            return response.json()
        else:
            logging.error(f"Product retrieval failed with status {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Product retrieval error - {str(e)}")
        return []

def create_product(token: str) -> Dict[str, Any]:
    """Create a product with error simulation"""
    if simulate_error():
        logging.error("Simulated error during product creation")
        return None
        
    product_data = {
        "name": f"Product {random.randint(1, 1000)}",
        "description": f"Description for product {random.randint(1, 1000)}",
        "price": round(random.uniform(10.0, 1000.0), 2),
        "stock": random.randint(0, 100),
        "category": random.choice(["Electronics", "Clothing", "Books", "Home", "Sports"])
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{PRODUCT_SERVICE_URL}", json=product_data, headers=headers)
        if response.status_code == 201:
            logging.info("Product created successfully")
            return response.json()
        else:
            logging.error(f"Product creation failed with status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Product creation error - {str(e)}")
        return None

def update_product(product_id: int, token: str) -> Dict[str, Any]:
    """Update a product with error simulation"""
    if simulate_error():
        logging.error(f"Simulated error during product update for ID {product_id}")
        return None
        
    update_data = {
        "name": f"Updated Product {product_id}",
        "price": round(random.uniform(10.0, 1000.0), 2),
        "stock": random.randint(0, 100),
        "description": f"Updated description for product {product_id}"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.put(f"{PRODUCT_SERVICE_URL}/{product_id}", json=update_data, headers=headers)
        if response.status_code == 200:
            logging.info(f"Product {product_id} updated successfully")
            return response.json()
        else:
            logging.error(f"Product update failed with status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Product update error - {str(e)}")
        return None

def delete_product(product_id: int, token: str) -> bool:
    """Delete a product with error simulation"""
    if simulate_error():
        logging.error(f"Simulated error during product deletion for ID {product_id}")
        return False
        
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(f"{PRODUCT_SERVICE_URL}/{product_id}", headers=headers)
        if response.status_code == 204:
            logging.info(f"Product {product_id} deleted successfully")
            return True
        else:
            logging.error(f"Product deletion failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Product deletion error - {str(e)}")
        return False

def user_session(user_id: int):
    """Simulate a user session with error simulation"""
    max_retries = 3
    retry_count = 0
    retry_delays = [2, 5, 10]  # Increasing delays between retries: 2s, 5s, 10s
    
    while retry_count < max_retries:
        try:
            # Add initial delay before starting session (1-3 seconds)
            time.sleep(random.uniform(1, 3))
            
            # Register user (only if not already registered)
            if random.random() < 0.3:  # 30% chance to try registration
                user = register_user(user_id)
                if not user:
                    logging.warning(f"User {user_id}: Registration failed, will try login")
                else:
                    logging.info(f"User {user_id}: Registration successful")
                # Add delay after registration attempt (1-2 seconds)
                time.sleep(random.uniform(1, 2))

            # Login (will try even if registration failed)
            token = login_user(user_id)
            if not token:
                logging.warning(f"User {user_id}: Login failed, retrying...")
                retry_count += 1
                time.sleep(retry_delays[min(retry_count - 1, len(retry_delays) - 1)])
                continue

            # Add delay after successful login (2-4 seconds)
            time.sleep(random.uniform(2, 4))

            # Get user profile
            profile = get_user_profile(user_id, token)
            if not profile:
                logging.warning(f"User {user_id}: Profile retrieval failed, continuing with other operations")
            # Add delay after profile retrieval (1-3 seconds)
            time.sleep(random.uniform(1, 3))

            # Get products
            products = get_products(token)
            if not products:
                logging.warning(f"User {user_id}: Product listing failed, retrying...")
                time.sleep(retry_delays[min(retry_count - 1, len(retry_delays) - 1)])
                continue
            # Add delay after product listing (2-5 seconds)
            time.sleep(random.uniform(2, 5))

            # Create a product
            new_product = create_product(token)
            if not new_product:
                logging.warning(f"User {user_id}: Product creation failed, retrying...")
                time.sleep(retry_delays[min(retry_count - 1, len(retry_delays) - 1)])
                continue
            # Add delay after product creation (3-6 seconds)
            time.sleep(random.uniform(3, 6))

            # Update the product if we have one
            if new_product:
                updated_product = update_product(new_product["id"], token)
                if not updated_product:
                    logging.warning(f"User {user_id}: Product update failed for ID {new_product['id']}")
                # Add delay after product update (2-4 seconds)
                time.sleep(random.uniform(2, 4))

            # Delete the product if we have one
            if new_product:
                if not delete_product(new_product["id"], token):
                    logging.warning(f"User {user_id}: Product deletion failed for ID {new_product['id']}")
                # Add delay after product deletion (1-3 seconds)
                time.sleep(random.uniform(1, 3))

            # Successful session completed
            logging.info(f"User {user_id}: Session completed successfully")
            break

        except Exception as e:
            logging.error(f"User {user_id}: Unexpected error in session: {str(e)}")
            retry_count += 1
            time.sleep(retry_delays[min(retry_count - 1, len(retry_delays) - 1)])

    if retry_count >= max_retries:
        logging.error(f"User {user_id}: Session failed after {max_retries} retries")

    # Add a longer delay between sessions (5-15 seconds)
    time.sleep(random.uniform(5, 15))

def start_simulation():
    """Start the simulation with the configured number of users"""
    logging.info(f"Starting metrics simulator with {LOAD_PERCENTAGE}% load and {ERROR_PERCENTAGE}% error rate")
    logging.info(f"Maximum concurrent users: {MAX_USERS}")
    
    while True:
        try:
            # Calculate number of active users based on load percentage
            active_users = int((LOAD_PERCENTAGE / 100) * MAX_USERS)
            
            # Create threads for each active user
            threads = []
            for i in range(active_users):
                user_id = random.randint(1, 1000)
                thread = threading.Thread(target=user_session, args=(user_id,))
                threads.append(thread)
                thread.start()
                # Add a longer delay between thread starts (0.5-2 seconds)
                time.sleep(random.uniform(0.5, 2))
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Add a longer delay between batches (10-20 seconds)
            time.sleep(random.uniform(10, 20))
            
        except KeyboardInterrupt:
            logging.info("Simulation stopped by user")
            break
        except Exception as e:
            logging.error(f"Error in simulation: {str(e)}")
            time.sleep(10)  # Wait longer before retrying

if __name__ == "__main__":
    start_simulation() 