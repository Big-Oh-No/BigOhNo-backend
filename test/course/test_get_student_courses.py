from test.test_fixtures import *

def test_get_student_courses(authorized_client, test_enrollment):
    res = authorized_client.post("/course/student",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == 2

def test_get_student_courses_with_invalid_role(authorized_client, test_enrollment):
    res = authorized_client.post("/course/student",json={'email': 'teacher@korse.com', 'password': 'password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "User is not a student"

def test_get_tstudent_courses_with_invalid_user(authorized_client, test_enrollment):
    res = authorized_client.post("/course/student",json={'email': 'studentinvalid@korse.com', 'password': 'password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "Wrong email and password combination"
