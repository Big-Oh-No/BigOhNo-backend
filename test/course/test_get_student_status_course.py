from test.test_fixtures import *

def test_get_student_status_course(authorized_client, test_enrollment):
    res = authorized_client.post("/course/student_status",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert "July Frost" in [res.json()[0]["teacher_name"],res.json()[1]["teacher_name"]] 
    assert "Your preqs don't match." in [res.json()[0]["comment"],res.json()[1]["comment"]] 

def test_get_student_status_course_with_invalid_role(authorized_client, test_enrollment):
    res = authorized_client.post("/course/student_status",json={'email': 'teacher@korse.com', 'password': 'password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "User is not a student"

def test_get_student_status_course_with_invalid_user(authorized_client, test_enrollment):
    res = authorized_client.post("/course/student_status",json={'email': 'studentinvalid@korse.com', 'password': 'password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "Wrong email and password combination"


