-- DDW Wizard Simplified Test Data - Source Schema
-- Simplified database for VIDEX testing
-- Created: October 27, 2025
-- 
-- VIDEX supports the following index types:
-- ✅ Single-column indexes
-- ✅ Composite indexes
-- ✅ EXTENDED_KEYS indexes
-- ✅ Descending indexes
-- ❌ Not supported: Functional indexes, FULLTEXT, Spatial indexes

DROP DATABASE IF EXISTS ddw_test_src;
CREATE DATABASE IF NOT EXISTS ddw_test_src;
USE ddw_test_src;

-- Drop existing tables (in foreign key dependency order)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product_reviews;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;

-- =============================================================================
-- Core tables (6 tables - basic ecommerce scenario)
-- =============================================================================

-- 1. Categories table - Product categories table (with self-referencing foreign key)
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_parent_id (parent_id),
    INDEX idx_active (is_active),
    FOREIGN KEY (parent_id) REFERENCES categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Product categories hierarchy';

-- 2. Users table - User table (contains multiple index types)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other') DEFAULT 'Other',
    status ENUM('Active', 'Inactive', 'Pending') DEFAULT 'Pending',
    email_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_last_login (last_login),
    UNIQUE KEY uk_email_username (email, username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='User account management';

-- 3. Products table - Product table (FULLTEXT index and non-essential fields removed)
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT,
    brand VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2),
    status ENUM('Draft', 'Active', 'Inactive') DEFAULT 'Draft',
    stock_quantity INT DEFAULT 0,
    low_stock_threshold INT DEFAULT 10,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL,
    INDEX idx_sku (sku),
    INDEX idx_category (category_id),
    INDEX idx_status (status),
    INDEX idx_featured (featured)
    -- Note: FULLTEXT index removed because VIDEX does not support it
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Product catalog with essential information';

-- 4. Product reviews table - Product reviews table (testing many-to-many relationship)
CREATE TABLE product_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title VARCHAR(255),
    review_text TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_votes INT DEFAULT 0,
    status ENUM('Pending', 'Approved', 'Rejected', 'Spam') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id),
    INDEX idx_rating (rating),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Product reviews and ratings';

-- 5. Orders table - Orders table (core order information)
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Refunded') DEFAULT 'Pending',
    payment_status ENUM('Pending', 'Paid', 'Failed', 'Refunded', 'Partially_Refunded') DEFAULT 'Pending',
    currency VARCHAR(3) DEFAULT 'USD',
    subtotal DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    shipping_amount DECIMAL(12,2) DEFAULT 0.00,
    discount_amount DECIMAL(12,2) DEFAULT 0.00,
    total_amount DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    INDEX idx_order_number (order_number),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_payment_status (payment_status),
    INDEX idx_created_at (created_at),
    INDEX idx_total_amount (total_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Customer orders with essential information';

-- 6. Order items table - Order items table (many-to-many relationship intermediate table)
CREATE TABLE order_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    product_sku VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id),
    INDEX idx_product_sku (product_sku)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Individual items within orders';

-- =============================================================================
-- Example data insertion (optional)
-- =============================================================================

-- -- Insert category data
-- INSERT INTO categories (name, description, parent_id, is_active) VALUES
-- ('Electronics', 'Electronic devices and accessories', NULL, TRUE),
-- ('Computers', 'Desktop and laptop computers', 1, TRUE),
-- ('Smartphones', 'Mobile phones and accessories', 1, TRUE),
-- ('Clothing', 'Apparel and fashion items', NULL, TRUE),
-- ('Books', 'Physical and digital books', NULL, TRUE);

-- -- Insert user data
-- INSERT INTO users (username, email, password_hash, first_name, last_name, phone, status, email_verified) VALUES
-- ('john_doe', 'john@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'John', 'Doe', '555-0101', 'Active', TRUE),
-- ('jane_smith', 'jane@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Jane', 'Smith', '555-0102', 'Active', TRUE),
-- ('bob_wilson', 'bob@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Bob', 'Wilson', '555-0103', 'Active', TRUE),
-- ('alice_brown', 'alice@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Alice', 'Brown', '555-0104', 'Pending', FALSE),
-- ('charlie_davis', 'charlie@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Charlie', 'Davis', '555-0105', 'Active', TRUE);

-- -- Insert product data
-- INSERT INTO products (sku, name, description, category_id, brand, price, cost, status, stock_quantity, featured) VALUES
-- ('LAPTOP-001', 'Professional Laptop', 'High-performance laptop for professionals', 2, 'TechBrand', 1299.99, 899.99, 'Active', 50, TRUE),
-- ('PHONE-001', 'Smartphone Pro', 'Latest smartphone with advanced features', 3, 'PhoneCorp', 899.99, 599.99, 'Active', 100, TRUE),
-- ('LAPTOP-002', 'Gaming Laptop', 'High-end gaming laptop', 2, 'TechBrand', 1899.99, 1299.99, 'Active', 30, TRUE),
-- ('BOOK-001', 'Programming Guide', 'Comprehensive programming guide', 5, 'TechBooks', 49.99, 15.99, 'Active', 200, FALSE),
-- ('PHONE-002', 'Budget Smartphone', 'Affordable smartphone for everyday use', 3, 'PhoneCorp', 299.99, 199.99, 'Active', 150, FALSE);

-- -- Insert product review data
-- INSERT INTO product_reviews (product_id, user_id, rating, title, review_text, is_verified_purchase, status) VALUES
-- (1, 1, 5, 'Excellent laptop!', 'This laptop exceeded my expectations. Great performance and build quality.', TRUE, 'Approved'),
-- (1, 2, 4, 'Good value', 'Very good laptop for the price. Battery life could be better.', TRUE, 'Approved'),
-- (2, 1, 5, 'Best phone ever', 'Amazing phone with great camera and display.', TRUE, 'Approved'),
-- (2, 3, 3, 'Average phone', 'It works fine but nothing special. Expected more for the price.', TRUE, 'Approved'),
-- (3, 3, 5, 'Gaming beast!', 'Perfect for gaming. Runs all my games smoothly at max settings.', TRUE, 'Approved');

-- -- Insert order data
-- INSERT INTO orders (order_number, user_id, status, payment_status, currency, subtotal, tax_amount, shipping_amount, total_amount, payment_method) VALUES
-- ('ORD-100001', 1, 'Delivered', 'Paid', 'USD', 1299.99, 104.00, 0.00, 1403.99, 'Credit_Card'),
-- ('ORD-100002', 2, 'Shipped', 'Paid', 'USD', 899.99, 72.00, 15.99, 987.98, 'PayPal'),
-- ('ORD-100003', 3, 'Processing', 'Paid', 'USD', 1899.99, 151.99, 0.00, 2051.98, 'Credit_Card'),
-- ('ORD-100004', 1, 'Pending', 'Pending', 'USD', 49.99, 4.00, 5.99, 59.98, 'Credit_Card'),
-- ('ORD-100005', 3, 'Delivered', 'Paid', 'USD', 299.99, 24.00, 10.99, 334.98, 'Credit_Card');

-- -- Insert order items data
-- INSERT INTO order_items (order_id, product_id, product_sku, product_name, quantity, unit_price, total_price, tax_amount) VALUES
-- (1, 1, 'LAPTOP-001', 'Professional Laptop', 1, 1299.99, 1299.99, 104.00),
-- (2, 2, 'PHONE-001', 'Smartphone Pro', 1, 899.99, 899.99, 72.00),
-- (3, 3, 'LAPTOP-002', 'Gaming Laptop', 1, 1899.99, 1899.99, 151.99),
-- (4, 4, 'BOOK-001', 'Programming Guide', 1, 49.99, 49.99, 4.00),
-- (5, 5, 'PHONE-002', 'Budget Smartphone', 1, 299.99, 299.99, 24.00);
