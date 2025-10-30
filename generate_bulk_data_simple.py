#!/usr/bin/env python3
"""
Bulk Data Generator for DDL Wizard Test Database
Generates 500,000-1,000,000 rows per table with realistic data
"""

import random
import string
import hashlib
from datetime import datetime, timedelta
import json

# Configuration
NUM_CATEGORIES = 1000
NUM_USERS = 750000
NUM_PRODUCTS = 500000
NUM_ORDERS = 1000000
NUM_REVIEWS = 800000
# Removed: NUM_ADDRESSES, NUM_PAYMENT_METHODS (not in source_schema_simple.sql)

# Batch size for INSERT statements
BATCH_SIZE = 1000

# Data generation helpers
FIRST_NAMES = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
               'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica',
               'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
               'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley']

LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
              'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Walker', 'Hall', 'Allen']

BRANDS = ['TechBrand', 'ProElectronics', 'HomeStyle', 'GardenPro', 'BookWorld', 'FurniturePlus',
          'MobileTech', 'ComputerCorp', 'GadgetInc', 'StyleHome', 'OutdoorLiving', 'SmartDevices']

PRODUCT_ADJECTIVES = ['Premium', 'Deluxe', 'Professional', 'Advanced', 'Ultimate', 'Elite',
                      'Classic', 'Modern', 'Smart', 'Eco-Friendly', 'Portable', 'Wireless']

PRODUCT_TYPES = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones',
                 'Speaker', 'Camera', 'Printer', 'Chair', 'Desk', 'Lamp', 'Book', 'Shelf']

CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
          'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus',
          'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Boston', 'Portland',
          'Oklahoma City', 'Las Vegas', 'Detroit', 'Memphis', 'Louisville', 'Baltimore', 'Milwaukee']

STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
          'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
          'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
          'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

def random_date(start_year=2020, end_year=2025):
    """Generate random date between years"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def random_timestamp(start_year=2023, end_year=2025):
    """Generate random timestamp"""
    dt = random_date(start_year, end_year)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def random_email(username):
    """Generate random email"""
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'company.com']
    return f"{username}@{random.choice(domains)}"

def random_phone():
    """Generate random US phone number"""
    return f"+1-555-{random.randint(1000, 9999)}"

def random_password_hash():
    """Generate fake password hash"""
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

def write_batch(f, table_name, columns, values_list):
    """Write batch INSERT statement"""
    if not values_list:
        return
    
    f.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n")
    for i, values in enumerate(values_list):
        f.write(f"({values})")
        if i < len(values_list) - 1:
            f.write(",\n")
        else:
            f.write(";\n\n")

def generate_categories(f):
    """Generate category data"""
    print(f"Generating {NUM_CATEGORIES} categories...")
    
    columns = ['name', 'description', 'parent_id', 'is_active', 'created_at']
    batch = []
    
    for i in range(1, NUM_CATEGORIES + 1):
        name = f"Category_{i}_{random.choice(PRODUCT_TYPES)}"
        desc = f"Description for {name}"
        parent_id = random.randint(1, max(1, i-1)) if i > 100 and random.random() > 0.3 else 'NULL'
        is_active = 1 if random.random() > 0.1 else 0
        created_at = random_timestamp(2020, 2024)
        
        values = f"'{name}', '{desc}', {parent_id}, {is_active}, '{created_at}'"
        batch.append(values)
        
        if len(batch) >= BATCH_SIZE:
            write_batch(f, 'categories', columns, batch)
            batch = []
    
    if batch:
        write_batch(f, 'categories', columns, batch)

def generate_users(f):
    """Generate user data"""
    print(f"Generating {NUM_USERS} users...")
    
    columns = ['username', 'email', 'password_hash', 'first_name', 'last_name', 'phone',
               'date_of_birth', 'gender', 'status', 'email_verified', 'last_login', 
               'created_at']
    batch = []
    
    for i in range(1, NUM_USERS + 1):
        username = f"user{i}_{random.choice(string.ascii_lowercase)}{random.randint(100,999)}"
        email = random_email(username)
        password_hash = random_password_hash()
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        phone = random_phone()
        dob = random_date(1950, 2005).strftime('%Y-%m-%d')
        gender = random.choice(['Male', 'Female', 'Other'])
        status = random.choice(['Active', 'Active', 'Active', 'Inactive', 'Pending'])
        email_verified = 1 if random.random() > 0.2 else 0
        last_login = f"'{random_timestamp(2024, 2025)}'" if random.random() > 0.3 else 'NULL'
        created_at = random_timestamp(2020, 2024)
        
        values = f"'{username}', '{email}', '{password_hash}', '{first_name}', '{last_name}', '{phone}', '{dob}', '{gender}', '{status}', {email_verified}, {last_login}, '{created_at}'"
        batch.append(values)
        
        if len(batch) >= BATCH_SIZE:
            write_batch(f, 'users', columns, batch)
            batch = []
        
        if i % 50000 == 0:
            print(f"  Generated {i} users...")
    
    if batch:
        write_batch(f, 'users', columns, batch)

# Removed: generate_user_profiles() - table not in source_schema_simple.sql

def generate_products(f):
    """Generate product data"""
    print(f"Generating {NUM_PRODUCTS} products...")
    
    columns = ['sku', 'name', 'description', 'category_id', 'brand', 'price', 'cost',
               'status', 'stock_quantity', 'low_stock_threshold', 'featured', 'created_at']
    batch = []
    
    for i in range(1, NUM_PRODUCTS + 1):
        sku = f"SKU{i:08d}"
        name = f"{random.choice(PRODUCT_ADJECTIVES)} {random.choice(PRODUCT_TYPES)} {i}"
        description = f"Detailed description for {name}"
        category_id = random.randint(1, min(NUM_CATEGORIES, 1000))
        brand = random.choice(BRANDS)
        price = round(random.uniform(9.99, 2999.99), 2)
        cost = round(price * random.uniform(0.4, 0.7), 2)
        status = random.choice(['Active', 'Active', 'Active', 'Draft', 'Inactive'])
        stock_qty = random.randint(0, 500)
        low_threshold = 10
        featured = 1 if random.random() > 0.9 else 0
        created_at = random_timestamp(2020, 2024)
        
        values = f"'{sku}', '{name}', '{description}', {category_id}, '{brand}', {price}, {cost}, '{status}', {stock_qty}, {low_threshold}, {featured}, '{created_at}'"
        batch.append(values)
        
        if len(batch) >= BATCH_SIZE:
            write_batch(f, 'products', columns, batch)
            batch = []
        
        if i % 50000 == 0:
            print(f"  Generated {i} products...")
    
    if batch:
        write_batch(f, 'products', columns, batch)

def generate_orders(f):
    """Generate order data"""
    print(f"Generating {NUM_ORDERS} orders...")
    
    columns = ['order_number', 'user_id', 'status', 'payment_status', 'currency',
               'subtotal', 'tax_amount', 'shipping_amount', 'discount_amount', 'total_amount',
               'payment_method', 'created_at']
    batch = []
    
    statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Delivered', 'Delivered']
    payment_statuses = ['Paid', 'Paid', 'Paid', 'Pending', 'Failed']
    payment_methods = ['Credit_Card', 'Debit_Card', 'PayPal', 'Bank_Transfer']
    
    for i in range(1, NUM_ORDERS + 1):
        order_num = f"ORD{100000 + i}"
        user_id = random.randint(1, min(NUM_USERS, 750000))
        status = random.choice(statuses)
        payment_status = random.choice(payment_statuses)
        currency = 'USD'
        subtotal = round(random.uniform(20, 2000), 2)
        tax_amount = round(subtotal * 0.08, 2)
        shipping_amount = round(random.uniform(0, 25), 2)
        discount_amount = round(random.uniform(0, 50), 2)
        total_amount = subtotal + tax_amount + shipping_amount - discount_amount
        payment_method = random.choice(payment_methods)
        created_at = random_timestamp(2023, 2025)
        
        values = f"'{order_num}', {user_id}, '{status}', '{payment_status}', '{currency}', {subtotal}, {tax_amount}, {shipping_amount}, {discount_amount}, {total_amount}, '{payment_method}', '{created_at}'"
        batch.append(values)
        
        if len(batch) >= BATCH_SIZE:
            write_batch(f, 'orders', columns, batch)
            batch = []
        
        if i % 100000 == 0:
            print(f"  Generated {i} orders...")
    
    if batch:
        write_batch(f, 'orders', columns, batch)

def generate_order_items(f):
    """Generate order items data - 2-5 items per order"""
    print(f"Generating order items for {NUM_ORDERS} orders...")
    
    columns = ['order_id', 'product_id', 'product_sku', 'product_name', 'quantity',
               'unit_price', 'total_price', 'tax_amount', 'created_at']
    batch = []
    total_items = 0
    
    for order_id in range(1, NUM_ORDERS + 1):
        items_count = random.randint(2, 5)
        
        for _ in range(items_count):
            product_id = random.randint(1, min(NUM_PRODUCTS, 500000))
            product_sku = f"SKU{product_id:08d}"
            product_name = f"Product {product_id}"
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(9.99, 999.99), 2)
            total_price = round(unit_price * quantity, 2)
            tax_amount = round(total_price * 0.08, 2)
            created_at = random_timestamp(2023, 2025)
            
            values = f"{order_id}, {product_id}, '{product_sku}', '{product_name}', {quantity}, {unit_price}, {total_price}, {tax_amount}, '{created_at}'"
            batch.append(values)
            total_items += 1
            
            if len(batch) >= BATCH_SIZE:
                write_batch(f, 'order_items', columns, batch)
                batch = []
        
        if order_id % 100000 == 0:
            print(f"  Generated items for {order_id} orders ({total_items} items)...")
    
    if batch:
        write_batch(f, 'order_items', columns, batch)
    
    print(f"  Total order items generated: {total_items}")

def generate_reviews(f):
    """Generate product reviews"""
    print(f"Generating {NUM_REVIEWS} product reviews...")
    
    columns = ['product_id', 'user_id', 'rating', 'title', 'review_text', 
               'is_verified_purchase', 'helpful_votes', 'status', 'created_at']
    batch = []
    
    review_titles = ['Great product!', 'Love it', 'Awesome', 'Good value', 'Disappointed',
                     'Excellent quality', 'Worth the money', 'Not bad', 'Amazing', 'Perfect']
    
    for i in range(1, NUM_REVIEWS + 1):
        product_id = random.randint(1, min(NUM_PRODUCTS, 500000))
        user_id = random.randint(1, min(NUM_USERS, 750000))
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 5, 15, 30, 45])[0]
        title = random.choice(review_titles)
        review_text = f"Review text for product {product_id} by user {user_id}"
        is_verified = 1 if random.random() > 0.3 else 0
        helpful_votes = random.randint(0, 100)
        status = random.choice(['Approved', 'Approved', 'Approved', 'Pending'])
        created_at = random_timestamp(2023, 2025)
        
        values = f"{product_id}, {user_id}, {rating}, '{title}', '{review_text}', {is_verified}, {helpful_votes}, '{status}', '{created_at}'"
        batch.append(values)
        
        if len(batch) >= BATCH_SIZE:
            write_batch(f, 'product_reviews', columns, batch)
            batch = []
        
        if i % 100000 == 0:
            print(f"  Generated {i} reviews...")
    
    if batch:
        write_batch(f, 'product_reviews', columns, batch)

# Removed: generate_addresses() - table not in source_schema_simple.sql

# Removed: generate_payment_methods() - table not in source_schema_simple.sql

def main():
    """Main execution"""
    output_file = 'bulk_insert_data.sql'
    
    print(f"\n{'='*70}")
    print(f"DDL Wizard Bulk Data Generator")
    print(f"{'='*70}")
    print(f"\nGenerating data for:")
    print(f"  - {NUM_CATEGORIES:,} categories")
    print(f"  - {NUM_USERS:,} users")
    print(f"  - {NUM_PRODUCTS:,} products")
    print(f"  - {NUM_ORDERS:,} orders")
    print(f"  - ~{NUM_ORDERS * 3:,} order items (2-5 per order)")
    print(f"  - {NUM_REVIEWS:,} product reviews")
    print(f"\nOutput file: {output_file}")
    print(f"{'='*70}\n")
    
    start_time = datetime.now()
    
    with open(output_file, 'w') as f:
        f.write("-- Bulk Insert Data for DDL Wizard Test Database\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total records: ~{NUM_USERS + NUM_PRODUCTS + NUM_ORDERS + NUM_REVIEWS:,}\n\n")
        f.write("USE ddw_test_src;\n\n")
        f.write("-- Disable foreign key checks for faster insertion\n")
        f.write("SET FOREIGN_KEY_CHECKS=0;\n")
        f.write("SET UNIQUE_CHECKS=0;\n")
        f.write("SET AUTOCOMMIT=0;\n\n")
        
        # Generate parent tables first
        generate_categories(f)
        f.write("COMMIT;\n\n")
        
        generate_users(f)
        f.write("COMMIT;\n\n")
        
        generate_products(f)
        f.write("COMMIT;\n\n")
        
        # Generate child tables
        generate_orders(f)
        f.write("COMMIT;\n\n")
        
        generate_order_items(f)
        f.write("COMMIT;\n\n")
        
        generate_reviews(f)
        f.write("COMMIT;\n\n")
        
        f.write("\n-- Re-enable checks and commit\n")
        f.write("COMMIT;\n")
        f.write("SET FOREIGN_KEY_CHECKS=1;\n")
        f.write("SET UNIQUE_CHECKS=1;\n")
        f.write("SET AUTOCOMMIT=1;\n\n")
        f.write("-- Data generation complete!\n")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n{'='*70}")
    print(f"Data generation complete!")
    print(f"Time taken: {duration:.2f} seconds")
    print(f"Output file: {output_file}")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
