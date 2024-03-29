from test.test_fixtures import *

def test_grade_submission(authorized_client, test_verified_teacher, test_submission, test_assignment, test_courses, test_verified_student_1):

    data={
        'assignment_id': test_assignment[0].id,
        'student_email': "student1@korse.com",
        'grade': 100,
        'email': 'teacher@korse.com',
        'password': 'password',
    }

    res = authorized_client.patch("/course/grade",data=data)

    assert res.status_code == 201