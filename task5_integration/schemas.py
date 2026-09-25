"""
Task 5: Pydantic Validation Schemas
Course: CSR210 - Advanced Programming & Databases
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of student", example="Priya Sharma")
    email: EmailStr = Field(..., description="Unique email address", example="priya.sharma@example.com")
    course: str = Field(..., min_length=2, max_length=100, description="Course name", example="B.Tech Data Science")
    marks: float = Field(..., ge=0.0, le=100.0, description="Marks percentage (0-100)", example=91.5)


class StudentCreate(StudentBase):
    """Schema for creating a student (POST). All fields required."""
    pass


class StudentUpdate(BaseModel):
    """Schema for updating a student (PUT). Fields can be partially provided."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    course: Optional[str] = Field(None, min_length=2, max_length=100)
    marks: Optional[float] = Field(None, ge=0.0, le=100.0)


class StudentResponse(StudentBase):
    """Schema returned to client including primary key ID."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None
