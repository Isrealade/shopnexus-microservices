#!/bin/bash

set -e
set -u

function create_database() {
    local database=$1
    echo "Creating database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO "$POSTGRES_USER";
EOSQL
}

function insert_test_data() {
    local database=$1
    echo "Inserting test data into '$database'"
    
    if [ "$database" = "users" ]; then
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$database" <<-EOSQL
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128) NOT NULL
            );
            
            -- Insert test users (password is 'testpass' for all users)
            INSERT INTO "user" (username, email, password_hash) VALUES
            ('testuser1', 'test1@example.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBAQKzqQZxKqHy'),
            ('testuser2', 'test2@example.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBAQKzqQZxKqHy'),
            ('testuser3', 'test3@example.com', '\$2b\$12\$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBAQKzqQZxKqHy')
            ON CONFLICT (username) DO NOTHING;
EOSQL
    elif [ "$database" = "products" ]; then
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$database" <<-EOSQL
            CREATE TABLE IF NOT EXISTS product (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                stock INTEGER NOT NULL,
                category VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Insert test products
            INSERT INTO product (name, description, price, stock, category) VALUES
            -- Computers & Laptops
            ('Laptop Pro', 'High-performance laptop with 16GB RAM and 512GB SSD', 1299.99, 50, 'Computers & Laptops'),
            ('Gaming Laptop', 'RGB gaming laptop with RTX 3080 and 32GB RAM', 1999.99, 25, 'Computers & Laptops'),
            ('Ultrabook Air', 'Ultra-thin laptop with 14-inch 4K display', 1499.99, 40, 'Computers & Laptops'),
            
            -- Monitors
            ('4K Monitor', '27-inch 4K UHD monitor with HDR support', 399.99, 30, 'Monitors'),
            ('Gaming Monitor', '32-inch 165Hz gaming monitor with G-Sync', 599.99, 20, 'Monitors'),
            ('Ultrawide Monitor', '34-inch curved ultrawide monitor', 499.99, 15, 'Monitors'),
            
            -- Peripherals
            ('Wireless Mouse', 'Ergonomic wireless mouse with long battery life', 29.99, 100, 'Peripherals'),
            ('Mechanical Keyboard', 'RGB mechanical keyboard with blue switches', 89.99, 75, 'Peripherals'),
            ('Gaming Headset', '7.1 surround sound gaming headset with noise cancellation', 79.99, 60, 'Peripherals'),
            ('Wireless Keyboard', 'Slim wireless keyboard with numeric pad', 49.99, 85, 'Peripherals'),
            ('Gaming Mouse', 'RGB gaming mouse with 20,000 DPI', 69.99, 45, 'Peripherals'),
            
            -- Audio
            ('Bluetooth Earbuds', 'True wireless earbuds with noise cancellation', 129.99, 70, 'Audio'),
            ('Studio Headphones', 'Professional studio headphones with flat response', 199.99, 30, 'Audio'),
            ('USB Microphone', 'Professional USB condenser microphone', 89.99, 40, 'Audio'),
            
            -- Storage
            ('1TB SSD', 'High-speed NVMe SSD with 3500MB/s read speed', 129.99, 100, 'Storage'),
            ('4TB External HDD', 'Portable external hard drive with USB 3.0', 99.99, 50, 'Storage'),
            ('2TB SSD', 'SATA SSD with 560MB/s read speed', 199.99, 60, 'Storage'),
            
            -- Networking
            ('WiFi Router', 'Dual-band WiFi 6 router with mesh support', 149.99, 35, 'Networking'),
            ('Network Switch', '8-port gigabit network switch', 49.99, 45, 'Networking'),
            ('WiFi Extender', 'Dual-band WiFi range extender', 39.99, 55, 'Networking'),
            
            -- Accessories
            ('Laptop Stand', 'Adjustable aluminum laptop stand', 29.99, 80, 'Accessories'),
            ('USB Hub', '7-port USB 3.0 hub with power adapter', 24.99, 90, 'Accessories'),
            ('Monitor Arm', 'Gas spring monitor mount with cable management', 89.99, 25, 'Accessories'),
            ('Webcam', '1080p webcam with built-in microphone', 59.99, 40, 'Accessories'),
            ('Drawing Tablet', '10-inch drawing tablet with pressure sensitivity', 79.99, 30, 'Accessories')
            ON CONFLICT (id) DO NOTHING;
EOSQL
    fi
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        create_database $db
        insert_test_data $db
    done
    echo "Multiple databases created and populated with test data"
fi 