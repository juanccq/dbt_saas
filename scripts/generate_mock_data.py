import os
import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

fake = Faker()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=5432,
    database="saas_analytics",
    user=os.getenv("DB_USER", "dbt_admin"),
    password=os.getenv("DB_PASSWORD", "dbt_password")
)
cur = conn.cursor()

print("Creating table in 'raw' schema...")
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    DROP TABLE IF EXISTS raw.payments, raw.products, raw.clients, raw.employees, raw.sale_items,raw.sales CASCADE;

    CREATE TABLE raw.employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        role VARCHAR(50)
    );

    CREATE TABLE raw.clients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        created_at TIMESTAMP
    );

    CREATE TABLE raw.products (
        id SERIAL PRIMARY KEY,
        sku VARCHAR(255),
        name VARCHAR(255),
        unit_price DECIMAL(10, 2)
    );

    CREATE TABLE raw.sales (
        id SERIAL PRIMARY KEY,
        employee_id INT REFERENCES raw.employees(id),
        client_id INT REFERENCES raw.clients(id),
        sale_date DATE
    );

    CREATE TABLE raw.sale_items (
        id SERIAL PRIMARY KEY,
        sale_id INT REFERENCES raw.sales(id),
        product_id INT REFERENCES raw.products(id),
        quantity INT,
        price DECIMAL(10, 2)
    );
""")

print("Generating mock Clients and Subscriptions...")
cur.execute("INSERT INTO raw.employees (name, role) VALUES ('Alice', 'cashier') RETURNING id")
alice_id = cur.fetchone()[0]

employee_ids = [alice_id]
for _ in range(9):
    cur.execute("INSERT INTO raw.employees (name, role) VALUES (%s, %s) RETURNING id", 
                (fake.name(), random.choices(['cashier', 'branch_admin'], weights=[0.7, 0.3], k=1)[0]))
    employee_ids.append(cur.fetchone()[0])

client_ids = []
for _ in range(50):
    signup_date = fake.date_time_between(start_date='-2y', end_date='now')
    cur.execute("INSERT INTO raw.clients (name, email, created_at) VALUES (%s, %s, %s) RETURNING id",
                (fake.name(), fake.unique.email(), signup_date))
    client_ids.append(cur.fetchone()[0])

products = [
    ("SKU-1001", "Mechanical Keyboard", 120.00),
    ("SKU-1002", "Wireless Mouse", 45.00),
    ("SKU-1003", "USB-C Hub", 35.00),
    ("SKU-1004", "1080p Webcam", 60.00),
    ("SKU-1005", "Noise Cancelling Headphones", 250.00),
    ("SKU-1006", "External HDD 1Tb", 470.00),
    ("SKU-1007", "FullHD Monitor 24'", 380.00)
]
product_ids = []

for sku, name, price in products:
    cur.execute("INSERT INTO raw.products (sku, name, unit_price) VALUES (%s, %s, %s) RETURNING id",
                (sku, name, price))
    product_ids.append((cur.fetchone()[0], price))

for _ in range(150):
    rand_emp = random.choice(employee_ids)
    rand_client = random.choice(client_ids)
    rand_day = random.randint(1, 31)
    sale_date = f"2026-07-{rand_day:02d}"

    cur.execute("INSERT INTO raw.sales (employee_id, client_id, sale_date) VALUES (%s, %s, %s) RETURNING id",
                (rand_emp, rand_client, sale_date))
    sale_id = cur.fetchone()[0]

    num_items = random.randint(1, 4)
    for _ in range(num_items):
        prod_id, price = random.choice(product_ids)
        qty = random.randint(1, 2)

        cur.execute("INSERT INTO raw.sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (sale_id, prod_id, qty, price))

        if random.random() < 0.05:
            cur.execute("INSERT INTO raw.sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                        (sale_id, prod_id, qty, price))

# Force some guaranteed sales for Alice before and after her July 15th promotion
rand_client = random.choice(client_ids)
cur.execute("INSERT INTO raw.sales (employee_id, client_id, sale_date) VALUES (%s, %s, %s) RETURNING id", (alice_id, rand_client, '2026-07-05'))
sale_id = cur.fetchone()[0]
prod_id, price = random.choice(product_ids)
qty = random.randint(1, 2)
cur.execute("INSERT INTO raw.sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (sale_id, prod_id, qty, price))

conn.commit()
cur.close()
conn.close()
print("Data generation complete!")