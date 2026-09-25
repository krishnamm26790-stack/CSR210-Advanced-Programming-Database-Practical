"""
Task 5: Database Connection & FastAPI Dependency
Course: CSR210 - Advanced Programming & Databases
"""

import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(find_dotenv())

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "csr210_db")

# SQLAlchemy Database URL using psycopg2 driver
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

# Declarative Base
Base = declarative_base()


def get_db():
    """FastAPI Dependency for database session injection per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
