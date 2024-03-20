from test.test_fixtures import *

def test_approve_enrollment(authorized_client, test_enrollment, test_verified_admin_1):
    res = authorized_client.patch(f"/course/enrollment_update/0",json={'email': 'admin1@korse.com', 'password': 'password', 'student_id': test_enrollment[2].student_id, 'course_id': test_enrollment[2].course_id})

    assert res.status_code == 201
    assert test_enrollment[2].status == course_model.StatusEnum.approved

def test_decline_enrollment(authorized_client, test_enrollment, test_verified_admin_1):
    res = authorized_client.patch(f"/course/enrollment_update/1",json={'email': 'admin1@korse.com', 'password': 'password', 'student_id': test_enrollment[2].student_id, 'course_id': test_enrollment[2].course_id})

    assert res.status_code == 201
    assert test_enrollment[2].status == course_model.StatusEnum.declined

def test_invalid_enrollment(authorized_client, test_enrollment, test_verified_admin_1):
    res = authorized_client.patch(f"/course/enrollment_update/2",json={'email': 'admin1@korse.com', 'password': 'password', 'student_id': test_enrollment[2].student_id, 'course_id': test_enrollment[2].course_id})

    assert res.status_code == 422
    assert res.json()["detail"] == "dir must be either 0 or 1"

def test_enrollment_for_non_exisitant_entry(authorized_client, test_enrollment, test_verified_admin_1):
    res = authorized_client.patch(f"/course/enrollment_update/0",json={'email': 'admin1@korse.com', 'password': 'password', 'student_id': test_enrollment[2].student_id + 1, 'course_id': test_enrollment[2].course_id - 1})

    assert res.status_code == 404
    assert res.json()["detail"] == "no such enrollment request found"