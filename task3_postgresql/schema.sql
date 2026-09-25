-- CSR210: PostgreSQL Schema for Task 3
-- Database: csr210_db

-- 1. Create Database (Run this in default 'postgres' database if creating manually)
-- CREATE DATABASE csr210_db;

-- 2. Create Students Table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    course VARCHAR(100) NOT NULL,
    marks NUMERIC(5, 2) NOT NULL CHECK (marks >= 0 AND marks <= 100)
);

-- Sample Data (Optional)
INSERT INTO students (name, email, course, marks) VALUES
('Aarav Sharma', 'aarav.sharma@example.com', 'B.Tech CSE', 89.50),
('Diya Patel', 'diya.patel@example.com', 'B.Tech IT', 92.00)
ON CONFLICT (email) DO NOTHING;
