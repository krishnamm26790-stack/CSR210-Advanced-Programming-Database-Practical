"""
Task 1: Basic FastAPI Student Management Application
Course: CSR210 - Advanced Programming & Databases

Requirements:
1. GET / - Return a welcome message
2. GET /students - Return a list of students
3. GET /students/{id} - Return details of a student
4. POST /students - Add a new student
5. DELETE /students/{id} - Delete a student
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="CSR210 - Task 1: Basic FastAPI Student Management API",
    description="A simple, fast, and structured API managing students in-memory.",
    version="1.0.0"
)

# Pydantic Schemas
class Student(BaseModel):
    id: int = Field(..., description="Unique ID of the student", example=1)
    name: str = Field(..., min_length=2, max_length=100, description="Full name of student", example="John Doe")
    email: EmailStr = Field(..., description="Student email address", example="john.doe@example.com")
    course: str = Field(..., description="Course enrolled", example="B.Tech CSE")
    marks: float = Field(..., ge=0, le=100, description="Student marks (0-100)", example=88.5)

class StudentCreate(BaseModel):
    id: Optional[int] = Field(None, description="Optional ID (auto-generated if omitted)")
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    course: str
    marks: float = Field(..., ge=0, le=100)

# In-memory storage with initial sample data
students_db: List[dict] = [
    {"id": 1, "name": "Aarav Sharma", "email": "aarav.sharma@example.com", "course": "B.Tech CSE", "marks": 89.5},
    {"id": 2, "name": "Diya Patel", "email": "diya.patel@example.com", "course": "B.Tech IT", "marks": 92.0},
    {"id": 3, "name": "Rohan Verma", "email": "rohan.verma@example.com", "course": "MCA", "marks": 78.5},
    {"id": 4, "name": "Sneha Reddy", "email": "sneha.reddy@example.com", "course": "BCA", "marks": 85.0},
]


@app.get("/", tags=["General"])
def read_root():
    """1. GET / - Return a welcome message"""
    return {
        "message": "Welcome to CSR210 Student Management API (FastAPI)",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/students", response_model=List[Student], tags=["Students"])
def get_all_students():
    """2. GET /students - Return a list of all students"""
    return students_db


@app.get("/students/{id}", response_model=Student, tags=["Students"])
def get_student_by_id(id: int):
    """3. GET /students/{id} - Return details of a specific student"""
    for student in students_db:
        if student["id"] == id:
            return student
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with ID {id} not found."
    )


@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: StudentCreate):
    """4. POST /students - Add a new student"""
    # Auto-generate ID if not provided
    new_id = student.id
    if new_id is None:
        new_id = max([s["id"] for s in students_db], default=0) + 1
    else:
        # Check if ID already exists
        if any(s["id"] == new_id for s in students_db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID {new_id} already exists."
            )

    new_student = {
        "id": new_id,
        "name": student.name,
        "email": student.email,
        "course": student.course,
        "marks": student.marks
    }
    students_db.append(new_student)
    return new_student


@app.delete("/students/{id}", tags=["Students"])
def delete_student(id: int):
    """5. DELETE /students/{id} - Delete a student"""
    for index, student in enumerate(students_db):
        if student["id"] == id:
            deleted_student = students_db.pop(index)
            return {
                "message": f"Student with ID {id} successfully deleted.",
                "deleted_student": deleted_student
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with ID {id} not found."
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
