from test.test_fixtures import *

def test_user_login(authorized_client, test_verified_user):
    res = authorized_client.post("/user/login",json={'email': 'student@gmail.com', 'password': 'password'})
    assert res.status_code == 200
    assert res.json()["message"] == "User Authenticated"

def test_user_login_failed(authorized_client, test_verified_user):
    res = authorized_client.post("/user/login",json={'email': 'teacher@gmail.com', 'password': 'Password'})
    assert res.status_code == 409
    assert res.json()["detail"] == "Wrong email and password combination"

def test_user_login_failed_wrong_json(authorized_client, test_verified_user):
    res = authorized_client.post("/user/login",json={'password': 'Password'})
    assert res.status_code == 422