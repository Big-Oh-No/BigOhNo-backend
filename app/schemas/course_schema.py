from typing import Optional
from pydantic import BaseModel
from ..models import course_model

class Course(BaseModel):
    id: int
    dept: course_model.DeptEnum
    code: str
    name: str
    description: Optional[str]
    syllabus_url: Optional[str]
    image_url: Optional[str]
    term: course_model.TermEnum
    year: int
    credits: int
    total_seats: int
    taken_seats: int
    status: course_model.CourseStatusEnum
    teacher_name: str

    class Config:
        from_attributes = True

class CourseStatusStudent(BaseModel):
    id: int
    dept: course_model.DeptEnum
    code: str
    name: str
    description: Optional[str]
    syllabus_url: Optional[str]
    image_url: Optional[str]
    term: course_model.TermEnum
    year: int
    credits: int
    total_seats: int
    taken_seats: int
    teacher_name: str
    status: course_model.StatusEnum
    comment: Optional[str]

    class Config:
        from_attributes = True

class CourseEnrollmentView(BaseModel):
    student_id: int
    course_id: int
    first_name: str
    last_name: Optional[str]
    email: str
    dept: course_model.DeptEnum
    code: int
    year: int
    term: course_model.TermEnum

    class Config:
        from_attributes = True

class CourseEnrollmentUpdate(BaseModel):
    email: str
    password: str
    student_id: int
    course_id: int
    comment: Optional[str]

    class Config:
        from_attributes = True