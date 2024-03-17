from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..utils.db import get_db
from ..utils.utils import hash
from ..models import user_model, course_model
from ..schemas import user_schema, course_schema
from typing import List

router = APIRouter(
    prefix="/course",
    tags=["course"],
)

@router.post(
    "/teacher",
    status_code=200,
    response_model=List[course_schema.Course]
)
async def teacher_courses(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """ returns all assigned courses to a teacher """

    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    teacher = db.query(user_model.Teacher).filter(user_model.Teacher.user_id == user.id).first()

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is not a teacher"
        )
    
    my_courses = db.query(course_model.Course).filter(course_model.Course.teacher_id == teacher.id).all()

    return my_courses