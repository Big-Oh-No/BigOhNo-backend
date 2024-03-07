from app.utils.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

import app.models.user as user

def populatedb(db: Session = Depends(get_db)):
    # clear db
    db.query(user.User).delete()
    db.query(user.Teacher).delete()
    db.query(user.Student).delete()
    db.query(user.Admin).delete()
    db.commit()

    # create user
    user_1 = user.User(
        first_name = "Mrunal",
        last_name = "Mustapure",
        bio = "I am a second year student.",
        email = "moon@gmail.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user.Gender.female,
        pronouns = "She/Her",
        role = user.Role.student,
        verified = True
        )
    
    user_2 = user.User(
        first_name = "Arhaan",
        last_name = "Khaku",
        bio = "I am a second year student.",
        email = "arhaan.khaku@gmail.com",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user.Gender.male,
        pronouns = "He/Him/His",
        role = user.Role.student,
        verified = False
        )
    
    user_3 = user.User(
        first_name = "Anand",
        bio = "I am an admin.",
        email = "a@mail.ubc.ca",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user.Gender.male,
        pronouns = "He/Him/His",
        role = user.Role.admin,
        verified = True
        )
    
    user_4 = user.User(
        first_name = "Apoorva",
        last_name = "Devarakonda",
        bio = "I am a professor.",
        email = "apps@mail.ubc.ca",
        password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # password
        gender = user.Gender.female,
        pronouns = "He/Him/His",
        role = user.Role.teacher,
        verified = False
        )
    
    db.add(user_1)
    db.add(user_2)
    db.add(user_3)
    db.add(user_4)
    db.commit()
    db.refresh(user_1)
    db.refresh(user_2)
    db.refresh(user_3)
    db.refresh(user_4)

    # create student
    student_1 = user.Student(
        department = user.Department.science,
        year = 2,
        degree = user.Degree.bsc,
        user_id = user_1.id
    )
    student_2 = user.Student(
        department = user.Department.science,
        year = 2,
        degree = user.Degree.bsc,
        user_id = user_2.id
    )
    
    db.add(student_1)
    db.add(student_2)
    db.commit()
    db.refresh(student_1)
    db.refresh(student_2)

    # create admin
    admin_1 = user.Admin(
        contact = "1234567890",
        office = "Office 304, FIP Building",
        user_id = user_3.id
    )

    db.add(admin_1)
    db.commit()
    db.refresh(admin_1)

    # create teacher
    teacher_1 = user.Teacher(
        faculty = "Science and Engineering",
        office = "ASC 154",
        user_id = user_4.id
    )

    db.add(teacher_1)
    db.commit()
    db.refresh(teacher_1)

