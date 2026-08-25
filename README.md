# dbt Retail Analytics Pipeline

This repository contains a complete Data Engineering pipeline demonstrating how to transform raw retail data into analytics-ready models using **dbt**, **PostgreSQL**, and **Docker**.

## 1. Local Environment Setup

Before starting the database, you need to set up a Python virtual environment to run the mock data generator and handle local dependencies.

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

## 2. Docker & Database Configuration

This project relies on Docker to run PostgreSQL, Metabase, and dbt. For security, database credentials are managed via environment variables.

1. Create a `.env` file in the root of the project.
2. Add your local credentials to the `.env` file:

```
   POSTGRES_USER=db_user
   POSTGRES_PASSWORD=db_password
   POSTGRES_DB=db_name
```

3. Start the containers in detached mode:
   docker-compose up -d

## 3. Generate Mock Data

Once the database is running, execute the Python script to populate the raw schema with simulated retail data.

python scripts/generate_mock_data.py

## 4. Run & Test the dbt Pipeline

With the raw data in place, you can execute the dbt pipeline to clean, transform, and test the data.

# Build the models (Staging, Intermediate, and Marts)
dbt run

# Run the snapshot process for SCD Type 2 tracking
dbt snapshot

# Execute data quality tests
dbt test

## 5. Project Structure
```
.
├── docker-compose.yml          # Container orchestration (Postgres, Metabase, dbt)
├── .env                        # Secure environment variables (Do not commit to Git)
├── requirements.txt            # Python dependencies
├── scripts/
│   └── generate_mock_data.py   # Populates the raw database schema
└── dbt_project/
    ├── dbt_project.yml         # Main dbt configuration
    ├── profiles.yml            # Database connection profile referencing the .env
    ├── models/
    │   ├── staging/            # Initial cleanup, renaming, and deduplication
    │   ├── intermediate/       # Core business logic and table joins
    │   └── marts/              # Final aggregated tables ready for BI reporting
    ├── snapshots/              # Historical tracking logic (SCD Type 2)
    └── tests/                  # Custom data quality tests
```