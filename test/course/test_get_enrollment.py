from test.test_fixtures import *

def test_get_enrollment(authorized_client, test_enrollment, test_verified_admin_1):
    res = authorized_client.post("/course/enrollment_status",json={'email': 'admin1@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_enrollment_with_unverified_admin(authorized_client, test_enrollment, test_unverified_user):
    res = authorized_client.post("/course/enrollment_status",json={'email': 'admin1@gmail.com', 'password': 'password'})
    assert res.status_code == 417
    assert res.json()["detail"] == "User is not verified"
