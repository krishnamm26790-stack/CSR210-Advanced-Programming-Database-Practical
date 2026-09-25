"""
Task 4: SQLAlchemy Student Model
Course: CSR210 - Advanced Programming & Databases

Columns:
- id: Integer, Primary Key, Autoincrement
- name: String(100), Not Null
- email: String(120), Unique, Not Null
- course: String(100), Not Null
- marks: Float, Not Null
"""

from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    course = Column(String(100), nullable=False)
    marks = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint("marks >= 0 AND marks <= 100", name="check_valid_marks"),
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}', course='{self.course}', marks={self.marks})>"
