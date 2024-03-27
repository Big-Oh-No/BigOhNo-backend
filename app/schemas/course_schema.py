from datetime import date, datetime
from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel
from ..models import course_model
from ..models import user_model

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

    
class StudentAssignments(BaseModel):
    id: int
    title: str
    file_url: str
    deadline: datetime
    total_grade: float
    published: datetime
    grade: Optional[float]
    file_url: Optional[str]
    created_at: Optional[str]

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

class OneStudentCourse(BaseModel):
    role: user_model.RoleEnum
    meta: Course
    assignments: List[StudentAssignments]

    class Config:
        from_attributes = True

class OneStudentSubmission(BaseModel):
    student_email: str
    student_name: str
    grade: Optional[float]
    file_url: Optional[str]
    created_at: Optional[str]

    class Config:
        from_attributes = True

class TeacherAssignments(BaseModel):
    id: int
    title: str
    file_url: str
    deadline: datetime
    total_grade: float
    published: datetime
    responses: List[OneStudentSubmission]

    class Config:
        from_attributes = True

class OneTeacherCourse(BaseModel):
    role: user_model.RoleEnum
    meta: Course
    assignments: List[TeacherAssignments]

    class Config:
        from_attributes = True