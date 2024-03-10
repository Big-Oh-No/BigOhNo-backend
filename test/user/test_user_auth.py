from test.test_fixtures import *

def test_user_login(authorized_client, test_verified_user):
    res = authorized_client.post("/user/login",json={'email': 'student@gmail.com', 'password': 'password'})
    assert res.status_code == 200
    assert res.json()["message"] == "User Authenticated"