from test.test_fixtures import *

def test_get_courses(authorized_client, test_courses):
    res = authorized_client.post("/course/",json={'email': 'teacher@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == 4

def test_get_course_with_differnt_role(authorized_client, test_courses, test_verified_student_1):
    res = authorized_client.post("/course/",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == 4

def test_get_course_with_invalid_user(authorized_client, test_courses, test_verified_user):
    res = authorized_client.post("/course/",json={'email': 'teacherinvalid@korse.com', 'password': 'password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "Wrong email and password combination"
