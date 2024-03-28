from test.test_fixtures import *

def test_create_submission_new(authorized_client, test_assignment, test_enrollment, test_verified_student_1, test_courses):
    file_path = "assets/file_test.txt"

    data={
        'assignment_id': test_assignment[0].id,
        'email': 'student1@korse.com',
        'password': 'password',
    }

    res = authorized_client.post("/course/submit",data=data,files={'assignment_file': ("file_test.txt", open(file_path, "rb"))})

    assert res.status_code == 201
    assert res.json()["message"] == "submission added successfully"

def test_create_submission_update(authorized_client, test_submission, test_assignment, test_enrollment, test_verified_student_1, test_courses):
    file_path = "assets/file_test.txt"

    data={
        'assignment_id': test_assignment[0].id,
        'email': 'student1@korse.com',
        'password': 'password',
    }

    res = authorized_client.post("/course/submit",data=data,files={'assignment_file': ("file_test.txt", open(file_path, "rb"))})

    assert res.status_code == 201
    assert res.json()["message"] == "submission updated successfully"

def test_create_submission_past_time(authorized_client, test_submission_2, test_assignment_2, test_enrollment, test_verified_student_1, test_courses):
    file_path = "assets/file_test.txt"

    data={
        'assignment_id': test_assignment_2[0].id,
        'email': 'student1@korse.com',
        'password': 'password',
    }

    res = authorized_client.post("/course/submit",data=data,files={'assignment_file': ("file_test.txt", open(file_path, "rb"))})

    assert res.status_code == 406
    assert res.json()["detail"] == "Deadline passed"