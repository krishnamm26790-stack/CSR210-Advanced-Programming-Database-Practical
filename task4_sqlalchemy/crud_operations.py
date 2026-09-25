"""
Task 4: SQLAlchemy CRUD Operations & Session Handling
Course: CSR210 - Advanced Programming & Databases

Operations:
1. Create the table
2. Insert at least 5 students
3. Retrieve students
4. Update a student
5. Delete a student
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Student


def create_tables():
    """1. Create the tables defined in SQLAlchemy models."""
    print("[INFO] Creating database tables using SQLAlchemy Base.metadata.create_all()...")
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] Tables created successfully.")


def insert_students(db: Session, student_list: List[dict]):
    """2. Insert at least 5 students into the database."""
    created_students = []
    for data in student_list:
        # Check if student with email already exists
        existing = db.query(Student).filter(Student.email == data["email"]).first()
        if existing:
            print(f"[SKIP] Student with email '{data['email']}' already exists (ID: {existing.id}).")
            created_students.append(existing)
            continue

        student = Student(
            name=data["name"],
            email=data["email"],
            course=data["course"],
            marks=data["marks"]
        )
        db.add(student)
        db.flush()  # Flush to populate ID before commit
        created_students.append(student)
        print(f"[SUCCESS] Prepared student: {student.name} (ID: {student.id})")

    return created_students


def retrieve_students(db: Session, min_marks: Optional[float] = None) -> List[Student]:
    """3. Retrieve students from the database."""
    query = db.query(Student)
    if min_marks is not None:
        query = query.filter(Student.marks >= min_marks)
    students = query.order_by(Student.id.asc()).all()

    print("\n" + "=" * 70)
    print(f"{'ID':<6}{'Name':<22}{'Email':<28}{'Course':<15}{'Marks':<6}")
    print("-" * 70)
    for s in students:
        print(f"{s.id:<6}{s.name:<22}{s.email:<28}{s.course:<15}{s.marks:<6.1f}")
    print("=" * 70 + "\n")
    return students


def retrieve_student_by_id(db: Session, student_id: int) -> Optional[Student]:
    """Retrieve a single student by ID."""
    return db.query(Student).filter(Student.id == student_id).first()


def update_student(db: Session, student_id: int, **kwargs) -> Optional[Student]:
    """4. Update a student record."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        print(f"[NOT FOUND] Student with ID #{student_id} does not exist.")
        return None

    for key, value in kwargs.items():
        if hasattr(student, key) and value is not None:
            setattr(student, key, value)

    db.flush()
    print(f"[SUCCESS] Updated Student #{student_id}: {kwargs}")
    return student


def delete_student(db: Session, student_id: int) -> bool:
    """5. Delete a student record by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        print(f"[NOT FOUND] Student with ID #{student_id} does not exist.")
        return False

    db.delete(student)
    db.flush()
    print(f"[SUCCESS] Deleted Student #{student_id} ({student.name}).")
    return True


def main():
    print("--- CSR210 TASK 4: SQLAlchemy ORM Demonstration ---")
    
    # 1. Create table
    create_tables()

    # 2. Insert at least 5 students using session context manager
    initial_students = [
        {"name": "Ananya Sharma", "email": "ananya.sharma@example.com", "course": "B.Tech CSE", "marks": 94.5},
        {"name": "Bhavik Jain", "email": "bhavik.jain@example.com", "course": "B.Tech IT", "marks": 82.0},
        {"name": "Chetan Mehta", "email": "chetan.mehta@example.com", "course": "MCA", "marks": 76.0},
        {"name": "Divya Rao", "email": "divya.rao@example.com", "course": "BCA", "marks": 88.5},
        {"name": "Eshaan Kapoor", "email": "eshaan.kapoor@example.com", "course": "B.Tech AI", "marks": 91.0}
    ]

    print("\n[Step 2] Inserting 5 students with proper session handling...")
    with get_db() as db:
        insert_students(db, initial_students)

    # 3. Retrieve students
    print("\n[Step 3] Retrieving all students from database...")
    with get_db() as db:
        all_students = retrieve_students(db)

    # 4. Update a student
    if all_students:
        target_id = all_students[0].id
        print(f"\n[Step 4] Updating Student ID #{target_id}...")
        with get_db() as db:
            update_student(db, target_id, marks=98.0, course="B.Tech CSE (Honors)")
            retrieve_students(db)

    # 5. Delete a student
    if len(all_students) >= 5:
        delete_id = all_students[-1].id
        print(f"\n[Step 5] Deleting Student ID #{delete_id}...")
        with get_db() as db:
            delete_student(db, delete_id)
            retrieve_students(db)

    print("[DONE] Task 4 SQLAlchemy ORM demonstration complete.")


if __name__ == "__main__":
    main()
