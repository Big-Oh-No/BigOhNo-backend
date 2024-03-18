from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
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
    result = []
    for course in my_courses:
        result.append(course_schema.Course(
            id=course.id,
            dept=course.dept,
            code=course.code,
            name=course.name,
            description=course.description,
            syllabus_url=course.syllabus_url,
            image_url=course.image_url,
            term=course.term,
            year=course.year,
            credits=course.credits,
            total_seats=course.total_seats,
            taken_seats=course.taken_seats,
            status=course.status,
            teacher_name=f"{user.first_name} {user.last_name}"
        ))

    return result


@router.post(
    "/",
    status_code=200,
    response_model=List[course_schema.Course]
)
async def get_courses(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """ returns all active courses """

    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    courses = (
        db.query(
            course_model.Course.id,
            course_model.Course.dept,
            course_model.Course.code,
            course_model.Course.name,
            course_model.Course.description,
            course_model.Course.syllabus_url,
            course_model.Course.image_url,
            course_model.Course.term,
            course_model.Course.year,
            course_model.Course.credits,
            course_model.Course.total_seats,
            course_model.Course.taken_seats,
            course_model.Course.status,
            user_model.User.first_name,
            user_model.User.last_name)
        .join(user_model.Teacher, user_model.Teacher.id == course_model.Course.teacher_id)
        .join(user_model.User, user_model.User.id == user_model.Teacher.user_id)
        .filter(course_model.Course.status == course_model.CourseStatusEnum.active)
        .all()
    )

    result = []

    for course in courses:
        result.append(course_schema.Course(
            id=course.id,
            dept=course.dept,
            code=course.code,
            name=course.name,
            description=course.description,
            syllabus_url=course.syllabus_url,
            image_url=course.image_url,
            term=course.term,
            year=course.year,
            credits=course.credits,
            total_seats=course.total_seats,
            taken_seats=course.taken_seats,
            status=course.status,
            teacher_name=f"{course.first_name} {course.last_name}"
        ))

    return result


@router.post(
    "/student",
    status_code=200,
    response_model=List[course_schema.Course]
)
async def get_student_courses(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """ returns all student courses that are approved """

    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    student = db.query(user_model.Student).filter(user_model.Student.user_id == user.id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is not a student"
        )

    courses = (
        db.query(
            course_model.Course.id,
            course_model.Course.dept,
            course_model.Course.code,
            course_model.Course.name,
            course_model.Course.description,
            course_model.Course.syllabus_url,
            course_model.Course.image_url,
            course_model.Course.term,
            course_model.Course.year,
            course_model.Course.credits,
            course_model.Course.total_seats,
            course_model.Course.taken_seats,
            course_model.Course.status,
            user_model.User.first_name,
            user_model.User.last_name)
        .join(course_model.Enrollment, course_model.Enrollment.course_id == course_model.Course.id)
        .join(course_model.Student, course_model.Enrollment.student_id == course_model.Student.id)
        .join(user_model.Teacher, user_model.Teacher.id == course_model.Course.teacher_id)
        .join(user_model.User, user_model.User.id == user_model.Teacher.user_id)
        .filter(course_model.Enrollment.status == course_model.StatusEnum.approved)
        .all()
    )

    result = []

    for course in courses:
        result.append(course_schema.Course(
            id=course.id,
            dept=course.dept,
            code=course.code,
            name=course.name,
            description=course.description,
            syllabus_url=course.syllabus_url,
            image_url=course.image_url,
            term=course.term,
            year=course.year,
            credits=course.credits,
            total_seats=course.total_seats,
            taken_seats=course.taken_seats,
            status=course.status,
            teacher_name=f"{course.first_name} {course.last_name}"
        ))

    return result


@router.post(
    "/student_status",
    status_code=200,
    response_model=List[course_schema.CourseStatusStudent]
)
async def get_student_status_courses(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """ returns all student courses that are pending or rejected """

    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    student = db.query(user_model.Student).filter(user_model.Student.user_id == user.id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is not a student"
        )

    courses = (
        db.query(
            course_model.Course.id,
            course_model.Course.dept,
            course_model.Course.code,
            course_model.Course.name,
            course_model.Course.description,
            course_model.Course.syllabus_url,
            course_model.Course.image_url,
            course_model.Course.term,
            course_model.Course.year,
            course_model.Course.credits,
            course_model.Course.total_seats,
            course_model.Course.taken_seats,
            user_model.User.first_name,
            user_model.User.last_name,
            course_model.Enrollment.status,
            course_model.Enrollment.comment)
        .join(course_model.Enrollment, course_model.Enrollment.course_id == course_model.Course.id)
        .join(course_model.Student, course_model.Enrollment.student_id == course_model.Student.id)
        .join(user_model.Teacher, user_model.Teacher.id == course_model.Course.teacher_id)
        .join(user_model.User, user_model.User.id == user_model.Teacher.user_id)
        .filter(or_(course_model.Enrollment.status == course_model.StatusEnum.pending, course_model.Enrollment.status == course_model.StatusEnum.declined))
        .all()
    )

    result = []

    for course in courses:
        result.append(course_schema.CourseStatusStudent(
            id=course.id,
            dept=course.dept,
            code=course.code,
            name=course.name,
            description=course.description,
            syllabus_url=course.syllabus_url,
            image_url=course.image_url,
            term=course.term,
            year=course.year,
            credits=course.credits,
            total_seats=course.total_seats,
            taken_seats=course.taken_seats,
            teacher_name=f"{course.first_name} {course.last_name}",
            status=course.status,
            comment=course.comment
        ))

    return result