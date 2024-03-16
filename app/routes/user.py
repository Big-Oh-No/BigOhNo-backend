from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
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

    if user.role == user_model.Role.admin:
        admin = user_model.Admin(user_id = user.id)
        db.add(admin)
        db.commit()
        db.refresh(admin)
    elif user.role == user_model.Role.teacher:
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
    "/check",
    status_code=200,
    response_model=user_schema.UserVerificationCheck
)
async def check(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db)
):
    """ checks if a user is valid and verified """

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

    return user_schema.UserVerificationCheck(role=user.role)