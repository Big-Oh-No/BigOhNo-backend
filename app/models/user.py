from ..utils.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Enum, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
import enum


class Gender(enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class Role(enum.Enum):
    student = 'student'
    teacher = 'teacher'
    admin = 'admin'

class Department(enum.Enum):
    science = 'science'
    management = 'management'
    arts = 'arts'
    engineering = 'engineering'
    nursing = 'nursing'
    medicine = 'medicine'
    law = 'law'
    creative_studies = 'creative_studies'
    
class Degree(enum.Enum):
    bsc = 'bsc'
    ba = 'ba'

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String, nullable = False)
    last_name = Column(String)
    bio = Column(String)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    gender = Column(Enum(Gender))
    pronouns = Column(String)
    profile_image = Column(String)
    role = Column(Enum(Role), nullable=False)
    verified = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    
    
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    contact = Column(String)
    office = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)

    user = relationship("User", back_populates="admin")

    
class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    department = Column(Enum(Department))
    year = Column(Integer)
    degree = Column(Enum(Degree))
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    
    user = relationship("User", back_populates="student")

  
class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    faculty = Column(String)
    office = Column(String)
    contact = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
   
    user = relationship("User", back_populates="teacher")

User.teacher = relationship("Teacher", back_populates="user")
User.student = relationship("Student", back_populates="user")
User.admin = relationship("Admin", back_populates="user")