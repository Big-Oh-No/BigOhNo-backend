from test.test_fixtures import *

def test_get_course_student(authorized_client, test_courses, test_enrollment, test_submission,  test_verified_student_1):
    res = authorized_client.post(f"/course/{test_courses[0].id}",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 200

def test_get_course_student_when_not_approved(authorized_client, test_courses, test_submission,  test_verified_student_1):
    res = authorized_client.post(f"/course/{test_courses[0].id}",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 401