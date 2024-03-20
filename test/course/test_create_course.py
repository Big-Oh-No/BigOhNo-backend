from fastapi import UploadFile
from test.test_fixtures import *


def test_get_enrollment(authorized_client, test_verified_admin_1, test_verified_teacher):
    img_path = "assets/test.png"

    res = authorized_client.post("/course/create",
                                 data={
                                    'email': 'admin1@korse.com',
                                    'password': 'password',
                                    'dept': 'COSC',
                                    'code': '111',
                                    'course_name': 'Intro to coding',
                                    'description': 'Code with us',
                                    'term': 'W1',
                                    'year': 2024,
                                    'credits': 3,
                                    'total_seats': 100,
                                    'teacher_email': 'teacher@korse.com',
                                      },
                                files={'syllabus_file': ('dummy.pdf', b''), 'course_img': ("course_img.png", open(img_path, "rb"))}
    )
    
    assert res.status_code == 201

def test_get_enrollment_with_wrong_teacher(authorized_client, test_verified_admin_1):
    res = authorized_client.post("/course/create",
                                 data={
                                    'email': 'admin1@korse.com',
                                    'password': 'password',
                                    'dept': 'COSC',
                                    'code': '111',
                                    'course_name': 'Intro to coding',
                                    'description': 'Code with us',
                                    'term': 'W1',
                                    'year': 2024,
                                    'credits': 3,
                                    'total_seats': 100,
                                    'teacher_email': 'teacher@korse.com',
                                      },
                                files={'syllabus_file': ('dummy.pdf', b''), 'course_img': ('dummy.jpg', b'')}
                                 )
    assert res.status_code == 404
    assert res.json()["detail"] == "No such teacher found"
