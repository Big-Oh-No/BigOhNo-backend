from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..utils.db import get_db
from ..utils.utils import hash
from ..models import user_model
from ..schemas import user_schema
import re

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/login",
    status_code=200,
)
async def login(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """Logs a user in"""
    
    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    return {"message" : "User Authenticated"}



@router.post(
    "/signup",
    status_code=201
)
async def signup(
    info: user_schema.UserSignUp,
    db: Session = Depends(get_db)
):
    """ Create user account """

    if len(info.first_name) == 0 or not (all(char.isalpha() or char == "'" for char in info.first_name)):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid First Name"
        )
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    regex = re.compile(pattern)
    if not regex.match(info.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid Email Address"
        )

    if len(info.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Password must be at least 6 characters long"
        )
    
    user_exist = db.query(user_model.User).filter(user_model.User.email == info.email).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists"
        )

    user = user_model.User(
        first_name = info.first_name,
        last_name = info.last_name,
        email = info.email,
        password = hash(info.password), # password
        role = info.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    if user.role == user_model.RoleEnum.admin:
        admin = user_model.Admin(user_id = user.id)
        db.add(admin)
        db.commit()
        db.refresh(admin)
    elif user.role == user_model.RoleEnum.teacher:
        teacher = user_model.Teacher(user_id = user.id)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
    else:
        student = user_model.Student(user_id = user.id)
        db.add(student)
        db.commit()
        db.refresh(student)

    return {"message": "Account created successfully"}


@router.post(
    "/get_user",
    status_code=200,
)
async def get_user(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """ gets a user profile """
    
    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User is not verified"
        )
    
    user_json = user_schema.User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            bio=user.bio,
            email=user.email,
            gender=user.gender,
            pronouns=user.pronouns,
            profile_image=user.profile_image,
            role=user.role,
            verified=user.verified
        )
    
    if user.role == user_model.RoleEnum.admin:
        admin = db.query(user_model.Admin).filter(user_model.Admin.user_id == user.id).first()
        if not admin:
            raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unexpected error occured"
        )
        return user_schema.Admin(user=user_json, admin_id=admin.id, contact=admin.contact, office=admin.office)
        
    if user.role == user_model.RoleEnum.teacher:
        teacher = db.query(user_model.Teacher).filter(user_model.Teacher.user_id == user.id).first()
        if not teacher:
            raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unexpected error occured"
        )
        return user_schema.Teacher(user=user_json, teacher_id=teacher.id, faculty=teacher.faculty, office=teacher.office, contact=teacher.contact)
        
    if user.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(user_model.Student.user_id == user.id).first()
        if not student:
            raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unexpected error occured"
        )
        return user_schema.Student(user=user_json, student_id=student.id, department=student.department, year=student.year, degree=student.degree)
        
    raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unexpected error occured"
    )