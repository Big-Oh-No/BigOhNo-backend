from ..utils.db import Base
from .user_model import Student, Teacher
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Enum, Double, DATETIME
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
import enum

class DeptEnum(enum.Enum):
    cosc = "COSC"
    phys = "PHYS"
    biol = "BIOL"
    chem = "CHEM"
    math = "MATH"
    data = "DATA"
    stat = "STAT"

class TermEnum(enum.Enum):
    w_one = "W1"
    w_two = "W2"
    s_one = "S1"
    s_two = "S2"
   
class StatusEnum(enum.Enum):
    approved = "approved"
    declined = "declined"
    pending = "pending"

class CourseStatusEnum(enum.Enum):
    active = "active"
    closed = "closed"

    
class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    dept = Column(Enum(DeptEnum), nullable=False)
    code = Column(String, nullable=False) 
    name = Column(String, nullable=False) 
    description = Column(String)
    syllabus_url = Column(String)
    image_url = Column(String)
    term = Column(Enum(TermEnum), nullable=False)
    year = Column(Integer, nullable=False) 
    credits = Column(Integer, nullable=False) 
    total_seats = Column(Integer, nullable=False)
    taken_seats = Column(Integer, server_default="0", nullable=False)
    status = Column(Enum(CourseStatusEnum), server_default="active", nullable=False)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable=False)

    teacher = relationship("Teacher", back_populates="course")



class Enrollment(Base):
    __tablename__ = "enrollment"
    comment = Column(String)
    status = Column(Enum(StatusEnum), server_default="pending", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True, nullable=False)

    course = relationship("Course", back_populates="enrollment")
    student = relationship("Student", back_populates="enrollment")

class Assignment(Base):
    __tablename__ = "assignment"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    file_url = Column(String)
    deadline = Column(DATETIME, nullable=False)
    total_grade = Column(Double, nullable=False)
    published = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))




Teacher.course= relationship("Course", back_populates="teacher")
Course.enrollment = relationship("Enrollment", back_populates="course")
Student.enrollment = relationship("Enrollment", back_populates="student")