"""
Database Configuration for PostgreSQL connection.
Course: CSR210 - Advanced Programming & Databases
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load .env if present
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  # default or updated via .env
DB_NAME = os.getenv("DB_NAME", "csr210_db")


def get_connection(dbname: str = DB_NAME):
    """Establish and return a psycopg2 connection to PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=dbname
    )


def create_database_if_not_exists():
    """Ensure the target database exists; if not, create it."""
    try:
        # Connect to default 'postgres' database to check/create target database
        conn = get_connection(dbname="postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"[INFO] Database '{DB_NAME}' created successfully.")
        else:
            print(f"[INFO] Database '{DB_NAME}' already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[WARNING] Could not verify/create database: {e}")
