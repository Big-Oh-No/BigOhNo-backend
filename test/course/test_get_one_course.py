from test.test_fixtures import *

def test_get_course_student(authorized_client, test_courses, test_enrollment, test_submission, test_assignment, test_verified_student_1):
    res = authorized_client.post(f"/course/{test_courses[0].id}",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 200

def test_get_course_student_when_not_approved(authorized_client, test_courses, test_submission, test_assignment, test_verified_student_1):
    res = authorized_client.post(f"/course/{test_courses[0].id}",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 401

def test_get_course_teacher(authorized_client, test_courses, test_enrollment, test_submission, test_assignment, test_verified_teacher):
    res = authorized_client.post(f"/course/{test_courses[0].id}",json={'email': 'teacher@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()["assignments"]) == 2