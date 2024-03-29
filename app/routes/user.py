from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from ..utils.db import get_db
from ..utils.utils import hash
from ..models import user_model, course_model
from ..schemas import user_schema
from typing import List, Optional
import re

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

PORT_DATA = 8000
HOST = "0.0.0.0"


@router.post(
    "/login",
    status_code=200,
)
async def login(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),
):
    """Logs a user in"""

    user = db.query(user_model.User).filter(and_(user_model.User.email ==
                                                 user.email, user_model.User.password == hash(user.password))).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )

    return {"message": "User Authenticated"}


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

    user_exist = db.query(user_model.User).filter(
        user_model.User.email == info.email).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists"
        )

    user = user_model.User(
        first_name=info.first_name,
        last_name=info.last_name,
        email=info.email,
        password=hash(info.password),  # password
        role=info.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    if user.role == user_model.RoleEnum.admin:
        admin = user_model.Admin(user_id=user.id)
        db.add(admin)
        db.commit()
        db.refresh(admin)
    elif user.role == user_model.RoleEnum.teacher:
        teacher = user_model.Teacher(user_id=user.id)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
    else:
        student = user_model.Student(user_id=user.id)
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

    user = db.query(user_model.User).filter(and_(user_model.User.email ==
                                                 user.email, user_model.User.password == hash(user.password))).first()

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
        admin = db.query(user_model.Admin).filter(
            user_model.Admin.user_id == user.id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unexpected error occured"
            )
        return user_schema.Admin(user=user_json, admin_id=admin.id, contact=admin.contact, office=admin.office)

    if user.role == user_model.RoleEnum.teacher:
        teacher = db.query(user_model.Teacher).filter(
            user_model.Teacher.user_id == user.id).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unexpected error occured"
            )
        return user_schema.Teacher(user=user_json, teacher_id=teacher.id, faculty=teacher.faculty, office=teacher.office, contact=teacher.contact)

    if user.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(
            user_model.Student.user_id == user.id).first()
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


@router.post(
    "/verification_status",
    status_code=200,
    response_model=List[user_schema.UserVerifcationView]
)
async def verification_status(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),
):
    """ returns list of unverified users """

    user = db.query(user_model.User).filter(and_(user_model.User.email ==
                                                 user.email, user_model.User.password == hash(user.password))).first()

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

    if user.role != user_model.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User is not an admin"
        )

    query = (
        db
        .query(user_model.User)
        .filter(user_model.User.verified == False)
        .order_by(desc(user_model.User.created_at))
        .all()
    )

    return query


@router.patch(
    "/verify",
    status_code=200,
)
async def verify(
    user: user_schema.UserVerificationRequest,
    db: Session = Depends(get_db),
):
    """ Verifies a user """

    admin = db.query(user_model.User).filter(and_(user_model.User.email ==
                                                  user.email, user_model.User.password == hash(user.password))).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )

    if not admin.verified:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User is not verified"
        )

    if admin.role != user_model.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User is not an admin"
        )

    client_user = db.query(user_model.User).filter(
        user_model.User.email == user.user_email).first()

    if not client_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    client_user.verified = True
    db.commit()
    db.refresh(client_user)

    return {"message": "User Verified"}


@router.patch(
    "/edit",
    status_code=200,
)
async def edit_profile(
    email: str = Form(...),
    password: str = Form(...),

    bio: Optional[str] = Form(None),
    gender: Optional[user_model.GenderEnum] = Form(None),
    pronouns: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = Form(None),

    contact: Optional[str] = Form(None),
    office: Optional[str] = Form(None),

    department: Optional[user_model.DepartmentEnum] = Form(None),
    year: Optional[int] = Form(None),
    degree: Optional[user_model.DegreeEnum] = Form(None),

    faculty: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """ updates a user profile """

    user = db.query(user_model.User).filter(and_(
        user_model.User.email == email, user_model.User.password == hash(password))).first()

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

    user.bio = bio
    user.gender = gender
    user.pronouns = pronouns

    unique_suffix = f"{user.id}"
    profile_image_url = None

    if profile_image and profile_image.size != 0:
        profile_image_url = f"data/profile/{unique_suffix}{profile_image.filename}"
        with open(profile_image_url, "wb") as buffer:
            contents = await profile_image.read()
            buffer.write(contents)

    profile_image_file_url = None
    if profile_image_url:
        profile_image_file_url = f"http://{HOST}:{PORT_DATA}/{profile_image_url}"

    user.profile_image = profile_image_file_url

    db.commit()
    db.refresh(user)

    if user.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(
            user_model.Student.user_id == user.id).first()

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student Not Found"
            )

        student.department = department
        student.year = year
        student.degree = degree

        db.commit()
        db.refresh(student)

    elif user.role == user_model.RoleEnum.teacher:
        teacher = db.query(user_model.Teacher).filter(
            user_model.Teacher.user_id == user.id).first()

        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher Not Found"
            )

        teacher.contact = contact
        teacher.office = office
        teacher.faculty = faculty

        db.commit()
        db.refresh(teacher)

    elif user.role == user_model.RoleEnum.admin:
        admin = db.query(user_model.Admin).filter(
            user_model.Admin.user_id == user.id).first()

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin Not Found"
            )

        admin.contact = contact
        admin.office = office

        db.commit()
        db.refresh(admin)

    return {"message": "User Profile Updated Successfully"}


@router.post(
    "/deactivate_course",
    status_code=200,
)
async def deactivate_course(
    email: str,
    password: str,
    course_id: int,
    db: Session = Depends(get_db),
):
    """Check if valid user is admin"""

    admin = db.query(user_model.User).filter(user_model.User.email == email, user_model.User.password == hash(password), user_model.User.verified == True, user_model.User.role == user_model.RoleEnum.admin).first()
    if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not verified"
            )
    """Check if course exists"""
    course = db.query(course_model.Course).filter(course_model.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    course.status = course_model.CourseStatusEnum.closed
    db.commit()
    db.refresh(course)

    return {"Message" : "Course deacitvated successfully"}