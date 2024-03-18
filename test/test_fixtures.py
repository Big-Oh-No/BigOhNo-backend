import pytest
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.db import get_db, Base
from fastapi.testclient import TestClient
from app.models import user_model, course_model
from app.main import app

SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
test_engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

Test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=test_engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.expunge_all()
            session.close()

    client = TestClient(app)
    app.dependency_overrides[get_db] = override_get_db
    yield client

@pytest.fixture
def token():
    return "korse"

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

# does not add profile to role models
@pytest.fixture
def test_verified_user(session):
    user_data = [
        {
            "email": "student@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "I am a second year student.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.GenderEnum.male,
            "pronouns": "He/Him",
            "role": user_model.RoleEnum.student,
            "verified": True
        },
        {
            "email": "teacher@gmail.com",
            "first_name": "James",
            "last_name": "Potter",
            "bio": "I am a professor.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.GenderEnum.male,
            "pronouns": "He/Him",
            "role": user_model.RoleEnum.teacher,
            "verified": True
        },
        {
            "email": "admin@gmail.com",
            "first_name": "Dave",
            "last_name": "Madland",
            "bio": "I am Admin.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.GenderEnum.male,
            "pronouns": "He/Him",
            "role": user_model.RoleEnum.admin,
            "verified": True
        },
    ]

    def create_user(user_data):
        return user_model.User(**user_data)
    

    user_map = map(create_user, user_data)
    users = list(user_map)
    session.add_all(users)
    session.commit()
    users_list = session.query(user_model.User).all()
    return users_list



@pytest.fixture
def test_unverified_user(session):
    user_data = [
        {
            "email": "student1@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "I am a second year student.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.GenderEnum.male,
            "pronouns": "He/Him",
            "role": user_model.RoleEnum.student,
            "verified": False
        },
        {
            "email": "teacher1@gmail.com",
            "first_name": "James",
            "last_name": "Potter",
            "bio": "I am a professor.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.GenderEnum.male,
            "pronouns": "He/Him",
            "role": user_model.RoleEnum.teacher,
            "verified": False
        },
        {
            "email": "admin1@gmail.com",
            "first_name": "Dave",
            "last_name": "Madland",
            "bio": "I am Admin.",
            "password" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "gender": user_model.GenderEnum.male,
            "pronouns": "He/Him",
            "role": user_model.RoleEnum.admin,
        },
    ]

    def create_user(user_data):
        return user_model.User(**user_data)
    

    user_map = map(create_user, user_data)
    users = list(user_map)
    session.add_all(users)
    session.commit()
    users_list = session.query(user_model.User).all()
    return users_list

@pytest.fixture
def test_verified_teacher(session):
    user = user_model.User(
        first_name = "July",
        last_name = "Frost",
        bio = "I am a teacher.",
        email = "teacher@korse.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.female,
        pronouns = "She/Her",
        role = user_model.RoleEnum.teacher,
        verified = True
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    teacher = user_model.Teacher(
        faculty = "Science and Engineering",
        office = "ASC 154",
        contact = "1234567890",
        user_id = user.id
    )

    session.add(teacher)
    session.commit()
    session.refresh(teacher)

    return teacher

@pytest.fixture
def test_verified_teacher_2(session):
    user = user_model.User(
        first_name = "Quin",
        last_name = "Shaw",
        bio = "I am a teacher.",
        email = "teacher2@korse.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.female,
        pronouns = "She/Her",
        role = user_model.RoleEnum.teacher,
        verified = True
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    teacher = user_model.Teacher(
        faculty = "Science and Engineering",
        office = "ASC 154",
        contact = "1234567890",
        user_id = user.id
    )

    session.add(teacher)
    session.commit()
    session.refresh(teacher)

    return teacher

@pytest.fixture
def test_courses(session, test_verified_teacher, test_verified_teacher_2):
    course_1 = course_model.Course(
        dept=course_model.DeptEnum.cosc,
        code="111",
        name="Introduction to Programming",
        description="Introduction to the design, implementation, and understanding of computer programs. Topics include problem solving, algorithm design, and data and procedural abstraction, with emphasis on the development of working programs.",
        term=course_model.TermEnum.w_one,
        year=2024,
        credits=3,
        total_seats=100,
        status=course_model.CourseStatusEnum.active,
        teacher_id = test_verified_teacher.id
    )
    course_2 = course_model.Course(
        dept=course_model.DeptEnum.stat,
        code="230",
        name="Introductory Statistics",
        description="Applied statistics for students with a first-year calculus background. Estimation and testing of hypotheses, problem formulation, models and basic methods in analysis of variance, linear regression, and non-parametric methods. Descriptive statistics and probability are presented as a basis for such procedures.",
        term=course_model.TermEnum.w_one,
        year=2024,
        credits=3,
        total_seats=60,
        status=course_model.CourseStatusEnum.active,
        teacher_id = test_verified_teacher.id
    )
    course_3 = course_model.Course(
        dept=course_model.DeptEnum.stat,
        code="303",
        name="Intermediate Probability",
        description="Multivariate probability distributions, moment and generating functions.",
        term=course_model.TermEnum.w_one,
        year=2024,
        credits=3,
        total_seats=30,
        status=course_model.CourseStatusEnum.active,
        teacher_id = test_verified_teacher.id
    )
    course_4 = course_model.Course(
        dept=course_model.DeptEnum.phys,
        code="304",
        name="Introduction to Quantum Mechanics",
        description="The beginnings of quantum mechanics, wave mechanics and the Schroedinger equation, one-dimensional potentials, the postulates of quantum mechanics, and applications to three-dimensional systems.",
        term=course_model.TermEnum.w_one,
        year=2024,
        credits=3,
        total_seats=30,
        status=course_model.CourseStatusEnum.active,
        teacher_id = test_verified_teacher_2.id
    )

    session.add(course_1)
    session.add(course_2)
    session.add(course_3)
    session.add(course_4)
    session.commit()

    return [course_1, course_2, course_3, course_4]

@pytest.fixture
def test_verified_student_1(session):
    user = user_model.User(
        first_name = "David",
        last_name = "Harrison",
        bio = "I am a student.",
        email = "student1@korse.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.male,
        pronouns = "He/Him/His",
        role = user_model.RoleEnum.student,
        verified = True
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    student = user_model.Student(
        department = user_model.DepartmentEnum.science,
        year = 2,
        degree = user_model.DegreeEnum.bsc,
        user_id = user.id
    )

    session.add(student)
    session.commit()
    session.refresh(student)

    return student

@pytest.fixture
def test_enrollment(session, test_courses, test_verified_student_1):
    enroll_1 = course_model.Enrollment(
        status=course_model.StatusEnum.approved,
        course_id=test_courses[0].id,
        student_id=test_verified_student_1.id
    )
    enroll_2 = course_model.Enrollment(
        status=course_model.StatusEnum.approved,
        course_id=test_courses[1].id,
        student_id=test_verified_student_1.id
    )
    enroll_3 = course_model.Enrollment(
        status=course_model.StatusEnum.pending,
        course_id=test_courses[2].id,
        student_id=test_verified_student_1.id
    )
    enroll_4 = course_model.Enrollment(
        comment="Your preqs don't match.",
        status=course_model.StatusEnum.declined,
        course_id=test_courses[3].id,
        student_id=test_verified_student_1.id
    )

    session.add(enroll_1)
    session.add(enroll_2)
    session.add(enroll_3)
    session.add(enroll_4)
    session.commit()
    session.refresh(enroll_1)
    session.refresh(enroll_2)
    session.refresh(enroll_3)
    session.refresh(enroll_4)

    return [enroll_1, enroll_2, enroll_3, enroll_4]

@pytest.fixture
def test_verified_admin_1(session):
    user = user_model.User(
        first_name = "James",
        last_name = "Bond",
        bio = "I am an admin.",
        email = "admin1@korse.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.male,
        pronouns = "He/Him/His",
        role = user_model.RoleEnum.admin,
        verified = True
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    admin = user_model.Admin(
        contact = "1234567890",
        office = "Office 125, SCI Building",
        user_id = user.id
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    return admin