from test.test_fixtures import *

def test_deactive_course(authorized_client, test_courses, test_verified_admin_1):

    data={
        'course_id': test_courses[0].id,
        'email': 'admin1@korse.com',
        'password': 'password',
    }
    
    res = authorized_client.post("/course/deactivate",data=data)

    assert res.status_code == 200