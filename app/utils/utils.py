from app.utils.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from hashlib import sha256

from ..models import user_model, course_model

def hash(password: str):
    return sha256(password.encode('utf-8')).hexdigest()

def populatedb(db: Session = Depends(get_db)):
    # clear db
    db.query(course_model.Enrollment).delete()
    db.query(user_model.Teacher).delete()
    db.query(course_model.Course).delete()
    db.query(user_model.Student).delete()
    db.query(user_model.Admin).delete()
    db.query(user_model.User).delete()
    db.commit()

    # create user
    user_1 = user_model.User(
        first_name = "Mrunal",
        last_name = "Mustapure",
        bio = "I am a second year student.",
        email = "moon@gmail.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.female,
        pronouns = "She/Her",
        role = user_model.RoleEnum.student,
        verified = True
        )
    
    user_2 = user_model.User(
        first_name = "Arhaan",
        last_name = "Khaku",
        bio = "I am a second year student.",
        email = "arhaan.khaku@gmail.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.male,
        pronouns = "He/Him/His",
        role = user_model.RoleEnum.student,
        verified = False
        )
    
    user_3 = user_model.User(
        first_name = "Anand",
        bio = "I am an admin.",
        email = "a@mail.ubc.ca",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.male,
        pronouns = "He/Him/His",
        role = user_model.RoleEnum.admin,
        verified = True
        )
    
    user_4 = user_model.User(
        first_name = "Apoorva",
        last_name = "Devarakonda",
        bio = "I am a professor.",
        email = "apps@mail.ubc.ca",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.female,
        pronouns = "She/Her",
        role = user_model.RoleEnum.teacher,
        verified = False
        )
    
    user_5 = user_model.User(
        first_name = "John",
        last_name = "Doe",
        bio = "I am an admin.",
        email = "admin@korse.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.male,
        pronouns = "He/Him/His",
        role = user_model.RoleEnum.admin,
        verified = True
    )

    user_6 = user_model.User(
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
    
    user_7 = user_model.User(
        first_name = "Adam",
        last_name = "Summer",
        bio = "I am a student.",
        email = "student@korse.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user_model.GenderEnum.male,
        pronouns = "He/Him/His",
        role = user_model.RoleEnum.student,
        verified = True
    )

    db.add(user_1)
    db.add(user_2)
    db.add(user_3)
    db.add(user_4)
    db.add(user_5)
    db.add(user_6)
    db.add(user_7)
    db.commit()
    db.refresh(user_1)
    db.refresh(user_2)
    db.refresh(user_3)
    db.refresh(user_4)
    db.refresh(user_5)
    db.refresh(user_6)
    db.refresh(user_7)

    # create student
    student_1 = user_model.Student(
        department = user_model.DepartmentEnum.science,
        year = 2,
        degree = user_model.DegreeEnum.bsc,
        user_id = user_1.id
    )
    student_2 = user_model.Student(
        department = user_model.DepartmentEnum.science,
        year = 2,
        degree = user_model.DegreeEnum.bsc,
        user_id = user_2.id
    )
    student_3 = user_model.Student(
        department = user_model.DepartmentEnum.science,
        year = 2,
        degree = user_model.DegreeEnum.bsc,
        user_id = user_7.id
    )
    
    db.add(student_1)
    db.add(student_2)
    db.add(student_3)
    db.commit()
    db.refresh(student_1)
    db.refresh(student_2)
    db.refresh(student_3)

    # create admin
    admin_1 = user_model.Admin(
        contact = "1234567890",
        office = "Office 304, FIP Building",
        user_id = user_3.id
    )
    admin_2 = user_model.Admin(
        contact = "1234567890",
        office = "Office 125, SCI Building",
        user_id = user_5.id
    )

    db.add(admin_1)
    db.add(admin_2)
    db.commit()
    db.refresh(admin_1)
    db.refresh(admin_2)

    # create teacher
    teacher_1 = user_model.Teacher(
        faculty = "Science and Engineering",
        office = "ASC 154",
        user_id = user_4.id
    )
    teacher_2 = user_model.Teacher(
        faculty = "Science and Engineering",
        office = "ASC 154",
        contact = "1234567890",
        user_id = user_6.id
    )

    db.add(teacher_1)
    db.add(teacher_2)
    db.commit()
    db.refresh(teacher_1)
    db.refresh(teacher_2)

    # add course
    course_1 = course_model.Course(
        dept=course_model.DeptEnum.cosc,
        code="111",
        name="Introduction to Programming",
        description="Introduction to the design, implementation, and understanding of computer programs. Topics include problem solving, algorithm design, and data and procedural abstraction, with emphasis on the development of working programs.",
        term=course_model.TermEnum.w_one,
        year="2024",
        credits=3,
        total_seats=100,
        status=course_model.CourseStatusEnum.active,
        teacher_id = teacher_2.id
    )
    course_2 = course_model.Course(
        dept=course_model.DeptEnum.stat,
        code="230",
        name="Introductory Statistics",
        description="Applied statistics for students with a first-year calculus background. Estimation and testing of hypotheses, problem formulation, models and basic methods in analysis of variance, linear regression, and non-parametric methods. Descriptive statistics and probability are presented as a basis for such procedures.",
        term=course_model.TermEnum.w_one,
        year="2024",
        credits=3,
        total_seats=60,
        status=course_model.CourseStatusEnum.active,
        teacher_id = teacher_2.id
    )
    course_3 = course_model.Course(
        dept=course_model.DeptEnum.stat,
        code="303",
        name="Intermediate Probability",
        description="Multivariate probability distributions, moment and generating functions.",
        term=course_model.TermEnum.w_one,
        year="2024",
        credits=3,
        total_seats=30,
        status=course_model.CourseStatusEnum.active,
        teacher_id = teacher_2.id
    )
    course_4 = course_model.Course(
        dept=course_model.DeptEnum.phys,
        code="304",
        name="Introduction to Quantum Mechanics",
        description="The beginnings of quantum mechanics, wave mechanics and the Schroedinger equation, one-dimensional potentials, the postulates of quantum mechanics, and applications to three-dimensional systems.",
        term=course_model.TermEnum.w_one,
        year="2024",
        credits=3,
        total_seats=30,
        status=course_model.CourseStatusEnum.active,
        teacher_id = teacher_1.id
    )

    db.add(course_1)
    db.add(course_2)
    db.add(course_3)
    db.add(course_4)
    db.commit()
    db.refresh(course_1)
    db.refresh(course_2)
    db.refresh(course_3)
    db.refresh(course_4)
