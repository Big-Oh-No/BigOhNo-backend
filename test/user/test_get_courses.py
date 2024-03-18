from test.test_fixtures import *

def test_get_teacher_courses(authorized_client, test_courses):
    res = authorized_client.post("/course/teacher",json={'email': 'teacher@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == 3

def test_get_teacher_course_with_invalid_role(authorized_client, test_courses, test_verified_user):
    res = authorized_client.post("/course/teacher",json={'email': 'teacher@gmail.com', 'password': 'password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "User is not a teacher"

def test_get_teacher_course_with_invalid_user(authorized_client, test_courses, test_verified_user):
    res = authorized_client.post("/course/teacher",json={'email': 'teacherinvalid@korse.com', 'password': 'password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "Wrong email and password combination"
