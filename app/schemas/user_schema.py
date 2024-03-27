from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from ..models import user_model, course_model

class UserSignIn(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class UserSignUp(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    password: str
    role: user_model.RoleEnum

    class Config:
        from_attributes = True

class UserVerificationCheck(BaseModel):
    role: user_model.RoleEnum

    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    bio: Optional[str]
    email: str
    gender: Optional[user_model.GenderEnum]
    pronouns: Optional[str]
    profile_image: Optional[str]
    role: user_model.RoleEnum
    verified: bool

    class Config:
        from_attributes = True

class Admin(BaseModel):
    user: User
    admin_id: int
    contact: Optional[str]
    office: Optional[str]

    class Config:
        from_attributes = True

class Teacher(BaseModel):
    user: User
    teacher_id: int
    faculty: Optional[str]
    office: Optional[str]
    contact: Optional[str]
    
    class Config:
        from_attributes = True

class Student(BaseModel):
    user: User
    student_id: int
    department: Optional[user_model.DepartmentEnum]
    year: Optional[int]
    degree: Optional[user_model.DegreeEnum]

    class Config:
        from_attributes = True

class UserVerifcationView(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    role: user_model.RoleEnum

    class Config:
        from_attributes = True

class UserVerificationRequest(BaseModel):
    email: str
    password: str
    user_email: str

    class Config:
        from_attributes = True
    
class UserEditProfileRequest(BaseModel):
    email: str
    password: str
    
    # common
    bio: Optional[str]
    gender: Optional[user_model.GenderEnum]
    pronouns: Optional[str]
    profile_image: Optional[UploadFile]

    # admin and teacher
    contact: Optional[str]
    office: Optional[str]

    # student
    department: Optional[user_model.DepartmentEnum]
    year: Optional[int]
    degree: Optional[user_model.DegreeEnum]

    # teacher
    faculty: Optional[str]

    class Config:
        from_attributes = True