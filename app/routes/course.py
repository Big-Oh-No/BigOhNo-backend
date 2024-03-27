from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, asc, func, or_
from ..utils.db import get_db
from ..utils.utils import hash
from ..models import user_model, course_model
from ..schemas import user_schema, course_schema
from typing import List, Optional
import socket

PORT_DATA = 8000
HOST = "0.0.0.0"

# def get_ipv4_address():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(("8.8.8.8", 80))
#         ipv4_address = s.getsockname()[0]
#         s.close()
#         return ipv4_address
#     except socket.error as e:
#         print("Socket error:", e)
#         return None
    
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
        .filter(and_(course_model.Enrollment.status == course_model.StatusEnum.approved,course_model.Enrollment.student_id==student.id))
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
        .filter(and_(or_(course_model.Enrollment.status == course_model.StatusEnum.pending, course_model.Enrollment.status == course_model.StatusEnum.declined),course_model.Enrollment.student_id==student.id))
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

@router.post(
    "/enroll/{course_id}",
    status_code=201
)
async def enroll(
    course_id: int,
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """ enrolls a student in a course """

    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is not verified yet"
        )
    
    student = db.query(user_model.Student).filter(user_model.Student.user_id == user.id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is not a student"
        )

    course = (
        db.query(course_model.Course)
        .filter(and_(course_model.Course.id == course_id, course_model.Course.status == course_model.CourseStatusEnum.active))
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such active course found"
        )
    
    if course.taken_seats == course.total_seats:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No seats available in the course"
        )
    
    check_enrollment = (
        db.query(course_model.Enrollment)
        .filter(and_(course_model.Enrollment.student_id==student.id, course_model.Enrollment.course_id==course_id))
        .first()
    )

    if check_enrollment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enrollment already exists"
        )


    enrollment_data = course_model.Enrollment(
        comment="Enrollment request is under review. Please contact admin@korse.com for more information.",
        course_id = course_id,
        student_id = student.id
    )

    db.add(enrollment_data)
    db.commit()
    db.refresh(enrollment_data)

    return {"message": "user enrollment request registered successfully"}

@router.post(
    "/enrollment_status",
    status_code=200,
    response_model=List[course_schema.CourseEnrollmentView]
)
async def enrollment_status(
    user: user_schema.UserSignIn,
    db: Session = Depends(get_db),    
):
    """ returns list of enrollment requests """
    
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
    
    if user.role != user_model.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User is not an admin"
        )

    query = (
        db.query(course_model.Enrollment.student_id, course_model.Enrollment.course_id, user_model.User.first_name, user_model.User.last_name, user_model.User.email, course_model.Course.dept, course_model.Course.code, course_model.Course.year, course_model.Course.term)
        .join(user_model.Student, user_model.User.id == user_model.Student.user_id)
        .join(course_model.Enrollment, user_model.Student.id == course_model.Enrollment.student_id)
        .join(course_model.Course, course_model.Course.id == course_model.Enrollment.course_id)
        .filter(course_model.Enrollment.status == course_model.StatusEnum.pending)
        .order_by(asc(course_model.Enrollment.created_at))
        .all()
    )

    return query



@router.patch(
    "/enrollment_update/{dir}",
    status_code=201,
)
async def enrollment_update(
    dir: int, # dir: 0 approve, 1: reject
    user: course_schema.CourseEnrollmentUpdate,
    db: Session = Depends(get_db),    
):
    """ updates the enrollment status of an enrollment request """
    
    admin = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

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

    
    course = db.query(course_model.Course).filter(course_model.Course.id == user.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no such course found"
        )

    decision = None


    if dir == 0:
        decision = course_model.StatusEnum.approved
        if course.total_seats == course.taken_seats:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no seats available"
        )
    elif dir == 1:
        decision = course_model.StatusEnum.declined
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="dir must be either 0 or 1"
        )

    query = (
        db
        .query(course_model.Enrollment)
        .filter(and_(course_model.Enrollment.student_id==user.student_id, course_model.Enrollment.course_id==user.course_id))
        .first()
    )

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no such enrollment request found"
        )
    
    if query.status == course_model.StatusEnum.approved and dir == 1:
        course.taken_seats -= 1
    elif query.status != course_model.StatusEnum.approved and dir == 0:
        course.taken_seats += 1
    
    db.commit()
    db.refresh(course)

    query.status = decision
    query.comment = user.comment
    db.commit()
    db.refresh(query)

    return {"message": "enrollment request processed successfully"}

@router.post(
    "/create",
    status_code=201
)
async def create(
    syllabus_file: Optional[UploadFile] = Form(...),
    course_img: Optional[UploadFile] = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    dept: course_model.DeptEnum = Form(...),
    code: str = Form(...),
    course_name: str = Form(...),
    description: str = Form(...),
    term: course_model.TermEnum = Form(...),
    year: int = Form(...),
    credits: int = Form(...),
    total_seats: int = Form(...),
    teacher_email: str = Form(...),
    db: Session = Depends(get_db)
):
    """ creates a new course """

    if total_seats <= 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Course must have at least 1 seat"
        )

    admin = db.query(user_model.User).filter(and_(user_model.User.email == email,user_model.User.password == hash(password))).first()

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
    
    teacher = db.query(user_model.Teacher).join(user_model.User, user_model.Teacher.user_id==user_model.User.id).filter(user_model.User.email==teacher_email).first()

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such teacher found"
        )
    
    course = db.query(course_model.Course).filter(and_(course_model.Course.term==term, course_model.Course.year==year, course_model.Course.dept==dept, course_model.Course.code==code, course_model.Course.teacher_id==teacher.id)).first()
    
    if course:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="course already exists"
        )
    
    unique_suffix = f"{dept}{code}{teacher.id}{term}{year}"
    syllabus_url=None
    image_url=None

    if syllabus_file and syllabus_file.size != 0:
        syllabus_url = f"data/syllabus/{unique_suffix}{syllabus_file.filename}"
        with open(syllabus_url, "wb") as buffer:
            contents = await syllabus_file.read()
            buffer.write(contents)
    
    if course_img and course_img.size != 0:
        image_url = f"data/courseimg/{unique_suffix}{course_img.filename}"
        with open(image_url, "wb") as buffer:
            contents = await course_img.read()
            buffer.write(contents)
    
    syllabus_file_url = None
    course_image_file_url = None
    if syllabus_url:
        syllabus_file_url = f"http://{HOST}:{PORT_DATA}/{syllabus_url}"
    if image_url:
        course_image_file_url = f"http://{HOST}:{PORT_DATA}/{image_url}"
    
    course_entry = course_model.Course(
        dept=dept,
        code=code,
        name=course_name,
        description=description,
        syllabus_url=syllabus_file_url,
        image_url=course_image_file_url,
        term=term,
        year=year,
        credits=credits,
        total_seats=total_seats,
        teacher_id=teacher.id
    )
    
    db.add(course_entry)
    db.commit()
    db.refresh(course_entry)

    return {"message": "course added successfully"}


@router.post(
    "/{id}",
    status_code=200,
    response_model=course_schema.OneStudentCourse | course_schema.OneTeacherCourse
)
async def get_courses(
    user: user_schema.UserSignIn,
    id: int,
    db: Session = Depends(get_db),    
):
    """ returns all active courses """

    user = db.query(user_model.User).filter(and_(user_model.User.email == user.email,user_model.User.password == hash(user.password))).first()

    if not user:
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong email and password combination"
        )
    
    course = db.query(course_model.Course).filter(course_model.Course.id == id).first()
    if not course:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Course not found"
        )
    
    teacher = db.query(user_model.Teacher).filter(user_model.Teacher.id == course.teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
            )
    
    teacher_profile = db.query(user_model.User).filter(user_model.User.id == teacher.user_id).first()
    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
            )
    
    if user.role == user_model.RoleEnum.student:
        student = db.query(user_model.Student).filter(user_model.Student.user_id == user.id).first()
        
        if not student:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
            )
        
        enrollment = db.query(course_model.Enrollment).filter(and_(course_model.Enrollment.student_id == student.id, course_model.Enrollment.course_id == course.id)).first()
        if not enrollment or enrollment.status != course_model.StatusEnum.approved:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied"
            )
        
        assigments = (
            db
            .query(
                course_model.Assignment.id,
                course_model.Assignment.title,
                course_model.Assignment.file_url,
                func.to_char(course_model.Assignment.deadline, 'YYYY-MM-DD HH24:MI:SS').label('deadline'),
                course_model.Assignment.total_grade,
                func.to_char(course_model.Assignment.published, 'YYYY-MM-DD HH24:MI:SS').label('published'),
                course_model.Submission.grade,
                course_model.Submission.file_url,
                func.to_char(course_model.Submission.created_at, 'YYYY-MM-DD HH24:MI:SS').label('created_at'),
            )
            .join(course_model.Submission, course_model.Assignment.id == course_model.Submission.assignment_id)
            .filter(and_(course_model.Assignment.course_id == course.id, course_model.Submission.student_id == student.id))
            .all()
        )

        response = course_schema.OneStudentCourse(
            role=user_model.RoleEnum.student,
            meta=course_schema.Course(
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
                teacher_name=f"{teacher_profile.first_name} {teacher_profile.last_name}"
            ),
            assignments=assigments
        )

        return response


    if user.role == user_model.RoleEnum.teacher:

        assigments = (
            db
            .query(
                course_model.Assignment.id,
                course_model.Assignment.title,
                course_model.Assignment.file_url,
                func.to_char(course_model.Assignment.deadline, 'YYYY-MM-DD HH24:MI:SS').label('deadline'),
                course_model.Assignment.total_grade,
                func.to_char(course_model.Assignment.published, 'YYYY-MM-DD HH24:MI:SS').label('published'),
            )
            .filter(course_model.Assignment.course_id == course.id)
            .all()
        )
        
        list_of_submission = []

        for assignment in assigments:
            res = (
                db
                .query(
                    course_model.Submission.grade,
                    course_model.Submission.file_url,
                    func.to_char(course_model.Submission.created_at, 'YYYY-MM-DD HH24:MI:SS').label('created_at'),
                    user_model.User.email.label("student_email"),
                    (user_model.User.first_name + ' ' + user_model.User.last_name).label("student_name")
                )
                .join(user_model.Student, user_model.Student.id == course_model.Submission.student_id)
                .join(user_model.User, user_model.User.id == user_model.Student.user_id)
                .filter(course_model.Submission.assignment_id == assignment.id)
                .all()
            )
        
            list_of_submission.append(
                course_schema.TeacherAssignments(
                    id=assignment.id,
                    title=assignment.title,
                    file_url=assignment.file_url,
                    deadline=assignment.deadline,
                    total_grade=assignment.total_grade,
                    published=assignment.published,
                    responses=res
                )
            )

        response = course_schema.OneTeacherCourse(
            role=user_model.RoleEnum.teacher,
            meta = course_schema.Course(
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
                teacher_name=f"{teacher_profile.first_name} {teacher_profile.last_name}"
            ),
            assignments = list_of_submission
        )   
        
        return response
    
    raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admins can't view course submissions"
            )