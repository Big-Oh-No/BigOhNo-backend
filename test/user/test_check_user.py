from test.test_fixtures import *

def test_check_user(authorized_client, test_verified_user):
    res = authorized_client.post("/user/check",json={'email': 'student@gmail.com', 'password': 'password'})
    assert res.status_code == 200
    assert res.json()["role"] == "student"

def test_check_user_when_not_verified(authorized_client, test_unverified_user):
    res = authorized_client.post("/user/check",json={'email': 'student1@gmail.com', 'password': 'password'})
    assert res.status_code == 417
    assert res.json()["detail"] == "User is not verified"

def test_check_user_with_wrong_creds(authorized_client, test_verified_user):
    res = authorized_client.post("/user/login",json={'email': 'student1@gmail.com', 'password': 'password1234'})
    assert res.status_code == 409
    assert res.json()["detail"] == "Wrong email and password combination"

def test_check_user_with_invalid_json(authorized_client, test_verified_user):
    res = authorized_client.post("/user/login",json={})
    assert res.status_code == 422