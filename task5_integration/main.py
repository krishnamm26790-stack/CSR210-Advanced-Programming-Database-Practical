"""
Task 5: Final Integrated Student Management API
Course: CSR210 - Advanced Programming & Databases

Stack:
FastAPI + PostgreSQL + SQLAlchemy + Pydantic

Endpoints:
1. POST /students - Create a student
2. GET /students - Get all students
3. GET /students/{id} - Get a student by ID
4. PUT /students/{id} - Update a student
5. DELETE /students/{id} - Delete a student
"""

from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas
import crud

# Ensure tables are created automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CSR210 - Student Management Production API",
    description="Full-stack API integrating FastAPI, PostgreSQL, SQLAlchemy ORM, and Pydantic validation.",
    version="2.0.0"
)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to CSR210 Task 5 Integrated Student Management API",
        "database": "PostgreSQL (SQLAlchemy ORM)",
        "docs_url": "/docs"
    }


# 1. POST /students - Create a student
@app.post(
    "/students",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    summary="Create a new student record"
)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Create a new student with email uniqueness validation."""
    # Check if student with this email already exists
    existing = crud.get_student_by_email(db, email=student.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with email '{student.email}' is already registered."
        )
    return crud.create_student(db=db, student=student)


# 2. GET /students - Get all students
@app.get(
    "/students",
    response_model=List[schemas.StudentResponse],
    tags=["Students"],
    summary="Retrieve all student records"
)
def get_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all students with optional pagination parameters."""
    return crud.get_students(db=db, skip=skip, limit=limit)


# 3. GET /students/{id} - Get a student by ID
@app.get(
    "/students/{id}",
    response_model=schemas.StudentResponse,
    tags=["Students"],
    summary="Retrieve a student by primary key ID"
)
def get_student(id: int, db: Session = Depends(get_db)):
    """Retrieve details of a single student by ID."""
    student = crud.get_student(db=db, student_id=id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {id} not found."
        )
    return student


# 4. PUT /students/{id} - Update a student
@app.put(
    "/students/{id}",
    response_model=schemas.StudentResponse,
    tags=["Students"],
    summary="Update an existing student record"
)
def update_student(id: int, student_update: schemas.StudentUpdate, db: Session = Depends(get_db)):
    """Update fields of an existing student. Returns 404 if not found."""
    # If email is being changed, verify uniqueness
    if student_update.email:
        existing_with_email = crud.get_student_by_email(db, email=student_update.email)
        if existing_with_email and existing_with_email.id != id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{student_update.email}' is already in use by another student."
            )

    updated_student = crud.update_student(db=db, student_id=id, student_update=student_update)
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {id} not found."
        )
    return updated_student


# 5. DELETE /students/{id} - Delete a student
@app.delete(
    "/students/{id}",
    response_model=schemas.MessageResponse,
    tags=["Students"],
    summary="Delete a student record"
)
def delete_student(id: int, db: Session = Depends(get_db)):
    """Delete an existing student record by ID."""
    deleted_student = crud.delete_student(db=db, student_id=id)
    if not deleted_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {id} not found."
        )
    return {
        "message": f"Student with ID {id} successfully deleted.",
        "detail": f"Removed record for '{deleted_student.name}' ({deleted_student.email})"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
