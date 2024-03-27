from test.test_fixtures import *

def test_create_assignment(authorized_client, test_verified_teacher, test_courses):
    file_path = "assets/file_test.txt"

    data={
        'course_id': 1,
        'title': 'New Assignment',
        'deadline': "2024-12-31",
        'total_grade': 100,
        'email': 'teacher@korse.com',
        'password': 'password',
    }

    res = authorized_client.post("/course/assignment",data=data,files={'assignment_file': ("file_test.txt", open(file_path, "rb"))})

    assert res.status_code == 201