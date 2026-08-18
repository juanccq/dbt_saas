import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="saas_analytics",
    user="dbt_admin",
    password="dbt_password"
)
cur = conn.cursor()

print("Creating table in 'raw' schema...")
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    DROP TABLE IF EXISTS raw.payments, raw.subscriptions, raw.users, raw.app_events, raw.employees, raw.sales;

    CREATE TABLE raw.employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        role VARCHAR(50)
    );

    CREATE TABLE raw.sales (
        id SERIAL PRIMARY KEY,
        employee_id INT REFERENCES raw.employees(id),
        amount DECIMAL(10,2),
        sale_date DATE
    );

    CREATE TABLE raw.users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255),
        email VARCHAR(255),
        signup_date TIMESTAMP
    );

    CREATE TABLE raw.app_events (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES raw.users(id),
        event_name VARCHAR(50),
        created_at TIMESTAMP
    );

    CREATE TABLE raw.subscriptions (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES raw.users(id),
        plan_name VARCHAR(50),
        monthly_rate DECIMAL(10,2),
        status VARCHAR(20)
    );

    CREATE TABLE raw.payments (
        id SERIAL PRIMARY KEY,
        subscription_id INT REFERENCES raw.subscriptions(id),
        amount DECIMAL(10,2),
        payment_date TIMESTAMP,
        status VARCHAR(20)
    );
""")

print("Generating mock Users and Subscriptions...")
plans = [('Basic', 9.99), ('Pro', 29.99), ('Enterprise', 99.99)]
statuses = ['active', 'active', 'active', 'canceled', 'past_due']

for _ in range(100):
    signup_date = fake.date_time_between(start_date='-2y', end_date='now')
    cur.execute("INSERT INTO raw.users (full_name, email, signup_date) VALUES (%s, %s, %s) RETURNING id",
                (fake.name(), fake.email(), signup_date))
    user_id = cur.fetchone()[0]

    plan = random.choice(plans)
    status = random.choice(statuses)
    cur.execute("INSERT INTO raw.subscriptions (user_id, plan_name, monthly_rate, status) VALUES (%s, %s, %s, %s) RETURNING id",
                (user_id, plan[0], plan[1], status))
    sub_id = cur.fetchone()[0]

    for i in range(random.randint(1, 12)):
        pay_date = signup_date + timedelta(days=30*1)
        if pay_date > datetime.now(): break
        pay_status = 'success' if random.random() > 0.1 else 'failed'
        cur.execute("INSERT INTO raw.payments (subscription_id, amount, payment_date, status) VALUES (%s, %s, %s, %s)",
                    (sub_id, plan[1], pay_date, pay_status))


event_types = ['login', 'view_dashboard', 'export_report', 'update_profile']
for _ in range(5000):
    rand_user = random.randint(1, 100)
    rand_date = fake.date_time_between(start_date='-1y', end_date='now')
    rand_event = random.choice(event_types)
    cur.execute("INSERT INTO raw.app_events (user_id, event_name, created_at) VALUES (%s, %s, %s)",
                (rand_user, rand_event, rand_date))

names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan', 'Fiona', 'George', 'Hannah', 'Ian', 'Julia']
employee_ids = []

for name in names:
    initial_role = 'cashier' if random.random() < 0.8 else 'branch_admin'
    cur.execute("INSERT INTO raw.employees (name, role) VALUES (%s, %s) RETURNING id", (name, initial_role))
    employee_ids.append(cur.fetchone()[0])

for _ in range(100):
    rand_emp = random.choice(employee_ids)
    rand_day = random.randint(1, 31)
    rand_amount = round(random.uniform(15.0, 250.0), 2)
    sale_date = f"2026-01-{rand_day:02d}"

    cur.execute("INSERT INTO raw.sales (employee_id, amount, sale_date) VALUES (%s, %s, %s)",
                (rand_emp, rand_amount, sale_date))

conn.commit()
cur.close()
conn.close()
print("Data generation complete!")