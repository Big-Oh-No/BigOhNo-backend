from test.test_fixtures import *

def test_verify_user(authorized_client, test_unverified_user, test_verified_admin_1):
    res = authorized_client.patch("/user/verify",json={'email': 'admin1@korse.com', 'password': 'password', 'user_email': test_unverified_user[0].email})
    assert res.status_code == 200
    assert test_unverified_user[0].verified

def test_verify_user_with_unverified_admin(authorized_client, test_unverified_user):
    res = authorized_client.patch("/user/verify",json={'email': test_unverified_user[2].email, 'password': 'password', 'user_email': test_unverified_user[0].email})
    assert res.status_code == 417
    assert res.json()["detail"]=="User is not verified"