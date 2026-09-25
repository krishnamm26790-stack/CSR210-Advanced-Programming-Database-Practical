"""
Task 3: PostgreSQL Raw Connection & CRUD Operations
Course: CSR210 - Advanced Programming & Databases

Database: csr210_db
Table: students (id, name, email, course, marks)

Operations:
1. Insert a student
2. Display students
3. Update a student
4. Delete a student
"""

import sys
import psycopg2
from psycopg2 import sql
from db_config import get_connection, create_database_if_not_exists


def create_table():
    """Create the students table if it doesn't already exist."""
    query = """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        course VARCHAR(100) NOT NULL,
        marks NUMERIC(5, 2) NOT NULL CHECK (marks >= 0 AND marks <= 100)
    );
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            print("[INFO] Table 'students' verified/created successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to create table: {e}")
        raise
    finally:
        conn.close()


def insert_student(name: str, email: str, course: str, marks: float):
    """1. Insert a student record into the students table."""
    query = """
    INSERT INTO students (name, email, course, marks)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (name, email, course, marks))
            student_id = cursor.fetchone()[0]
            conn.commit()
            print(f"[SUCCESS] Inserted student '{name}' with ID #{student_id}")
            return student_id
    except psycopg2.IntegrityError as ie:
        conn.rollback()
        print(f"[WARNING] Integrity error (possible duplicate email): {ie}")
        return None
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to insert student: {e}")
        return None
    finally:
        conn.close()


def display_students():
    """2. Display all student records."""
    query = "SELECT id, name, email, course, marks FROM students ORDER BY id ASC;"
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            print("\n" + "=" * 70)
            print(f"{'ID':<6}{'Name':<22}{'Email':<28}{'Course':<15}{'Marks':<6}")
            print("-" * 70)
            if not rows:
                print("No students found in the database.")
            for row in rows:
                print(f"{row[0]:<6}{row[1]:<22}{row[2]:<28}{row[3]:<15}{float(row[4]):<6.1f}")
            print("=" * 70 + "\n")
            return rows
    except Exception as e:
        print(f"[ERROR] Failed to display students: {e}")
        return []
    finally:
        conn.close()


def update_student(student_id: int, name: str = None, email: str = None, course: str = None, marks: float = None):
    """3. Update an existing student's details."""
    updates = []
    values = []

    if name is not None:
        updates.append("name = %s")
        values.append(name)
    if email is not None:
        updates.append("email = %s")
        values.append(email)
    if course is not None:
        updates.append("course = %s")
        values.append(course)
    if marks is not None:
        updates.append("marks = %s")
        values.append(marks)

    if not updates:
        print("[WARNING] No fields provided to update.")
        return False

    values.append(student_id)
    query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s RETURNING id;"

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            updated = cursor.fetchone()
            conn.commit()
            if updated:
                print(f"[SUCCESS] Student ID #{student_id} updated successfully.")
                return True
            else:
                print(f"[NOT FOUND] Student with ID #{student_id} does not exist.")
                return False
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to update student: {e}")
        return False
    finally:
        conn.close()


def delete_student(student_id: int):
    """4. Delete a student record by ID."""
    query = "DELETE FROM students WHERE id = %s RETURNING id;"
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (student_id,))
            deleted = cursor.fetchone()
            conn.commit()
            if deleted:
                print(f"[SUCCESS] Student ID #{student_id} deleted successfully.")
                return True
            else:
                print(f"[NOT FOUND] Student with ID #{student_id} not found.")
                return False
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to delete student: {e}")
        return False
    finally:
        conn.close()


def main():
    print("--- CSR210 TASK 3: PostgreSQL Raw Connection & CRUD Demonstration ---")
    create_database_if_not_exists()
    create_table()

    # 1. Insert Operation
    print("\n[Step 1] Inserting sample students...")
    s1 = insert_student("Kavya Nair", "kavya.nair@example.com", "B.Tech CSE", 91.5)
    s2 = insert_student("Aryan Gupta", "aryan.gupta@example.com", "MCA", 84.0)

    # 2. Display Operation
    print("\n[Step 2] Displaying all students...")
    display_students()

    # 3. Update Operation
    if s1:
        print(f"\n[Step 3] Updating Student ID #{s1} (Changing marks to 96.0)...")
        update_student(s1, marks=96.0, course="B.Tech CSE (Honors)")
        display_students()

    # 4. Delete Operation
    if s2:
        print(f"\n[Step 4] Deleting Student ID #{s2}...")
        delete_student(s2)
        display_students()

    print("[DONE] Task 3 CRUD demonstration complete.")


if __name__ == "__main__":
    main()
