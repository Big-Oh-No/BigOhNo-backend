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
    status: course_model.CourseStatusEnum
    teacher_name: str
    status: course_model.StatusEnum
    comment: Optional[str]

    class Config:
        from_attributes = True