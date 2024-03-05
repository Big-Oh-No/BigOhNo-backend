from ..utils.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean, Enum
from sqlalchemy.sql.expression import text
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


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    first_name = Column(String, nullable = False)
    last_name = Column(String)
    bio = Column(String)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    gender = Column(Enum(Gender))
    pronouns = Column(String)
    profile_image = Column(String)
    role = Column(Enum(Role))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    
    
class Admin(Base):
     __tablename__ = "admin"
     id = Column(String, ForeignKey('user.id'), primary_key=True, nullable=False)
     contact = Column(String)
     office = Column(String)
    
class Student(Base):
     __tablename__ = "student"
     id = Column(String, ForeignKey('user.id'), primary_key=True, nullable=False)
     department = Column(Enum(Department))
     year = Column(Integer)
     degree = Column(Enum(Degree))

  
class Teacher(Base):
     __tablename__ = "teacher"
     id = Column(String, ForeignKey('user.id'), primary_key=True, nullable=False)
     faculty = Column(String)
     office = Column(String)
     contact = Column(String)
    
    
     