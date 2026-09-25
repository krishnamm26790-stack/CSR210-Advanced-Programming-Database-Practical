"""
Task 5: CRUD Operations Layer
Course: CSR210 - Advanced Programming & Databases
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from models import Student
from schemas import StudentCreate, StudentUpdate


def get_student(db: Session, student_id: int) -> Optional[Student]:
    """Retrieve a single student by primary key ID."""
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    """Retrieve a student by email address."""
    return db.query(Student).filter(Student.email == email).first()


def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    """Retrieve a paginated list of students."""
    return db.query(Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: StudentCreate) -> Student:
    """Create a new student in the database."""
    db_student = Student(
        name=student.name,
        email=student.email,
        course=student.course,
        marks=student.marks
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student_update: StudentUpdate) -> Optional[Student]:
    """Update student attributes."""
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> Optional[Student]:
    """Delete a student record."""
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    db.delete(db_student)
    db.commit()
    return db_student
