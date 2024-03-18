from test.test_fixtures import *

def test_admin_view_for_verification(authorized_client, test_unverified_user, test_verified_admin_1):
    res = authorized_client.post("/user/verification_status",json={'email': 'admin1@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == len(test_unverified_user)

def test_admin_view_for_verification_with_all_verified(authorized_client, test_verified_user, test_verified_admin_1):
    res = authorized_client.post("/user/verification_status",json={'email': 'admin1@korse.com', 'password': 'password'})
    assert res.status_code == 200
    assert len(res.json()) == 0

def test_admin_view_for_verification_with_unverified_admin(authorized_client, test_unverified_user):
    res = authorized_client.post("/user/verification_status",json={'email': 'admin1@gmail.com', 'password': 'password'})
    assert res.status_code == 417
    assert res.json()["detail"] == "User is not verified"

def test_admin_view_for_verification_with_verified_student(authorized_client, test_verified_user, test_verified_student_1):
    res = authorized_client.post("/user/verification_status",json={'email': 'student1@korse.com', 'password': 'password'})
    assert res.status_code == 417
    assert res.json()["detail"] == "User is not an admin"

def test_admin_view_for_verification_with_wrong_auth(authorized_client, test_verified_user, test_verified_admin_1):
    res = authorized_client.post("/user/verification_status",json={'email': 'admin@korse.com', 'password': 'wrongpassword'})
    assert res.status_code == 409
    assert res.json()["detail"] == "Wrong email and password combination"

def test_cadmin_view_for_verification_with_invalid_json(authorized_client, test_verified_user):
    res = authorized_client.post("/user/get_user",json={})
    assert res.status_code == 422