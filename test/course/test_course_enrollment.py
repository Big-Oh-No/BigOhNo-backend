from test.test_fixtures import *

def test_course_enrollment_submission(authorized_client, test_courses, test_verified_student_1):
    res = authorized_client.post(f"/course/enroll/{test_courses[0].id}",json={'email': 'student1@korse.com', 'password': 'password'})
    res2 = authorized_client.post("/course/student_status",json={'email': 'student1@korse.com', 'password': 'password'})

    assert res.status_code == 201
    assert res2.status_code == 200
    assert len(res2.json()) == 1

def test_course_enrollment_submission_with_preenrollment(authorized_client, test_courses, test_verified_student_1):
    res = authorized_client.post(f"/course/enroll/{test_courses[0].id}",json={'email': 'student1@korse.com', 'password': 'password'})
    res2 = authorized_client.post(f"/course/enroll/{test_courses[0].id}",json={'email': 'student1@korse.com', 'password': 'password'})

    assert res.status_code == 201
    assert res2.status_code == 409
    assert res2.json()["detail"]=="Enrollment already exists"

def test_course_enrollment_submission_with_invalid_course(authorized_client, test_verified_student_1):
    res = authorized_client.post(f"/course/enroll/1",json={'email': 'student1@korse.com', 'password': 'password'})

    assert res.status_code == 404
    assert res.json()["detail"]=="No such active course found"

def test_course_enrollment_submission_with_teacher(authorized_client, test_courses, test_verified_teacher):
    res = authorized_client.post(f"/course/enroll/{test_courses[0].id}",json={'email': 'teacher@korse.com', 'password': 'password'})

    assert res.status_code == 409
    assert res.json()["detail"]=="User is not a student"

def test_course_enrollment_submission_with_unverfied_student(authorized_client, test_courses, test_unverified_user):
    res = authorized_client.post(f"/course/enroll/{test_courses[0].id}",json={'email': 'student1@gmail.com', 'password': 'password'})

    assert res.status_code == 409
    assert res.json()["detail"] == "User is not verified yet"