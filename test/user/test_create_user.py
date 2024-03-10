from test.test_fixtures import *

def test_create_user(authorized_client):
    data = {
        "first_name": "Adam",
        "last_name": "Bill",
        "email": "adam@gmail.com",
        "password": "password",
        "role": "admin"
    }

    response = authorized_client.post("/user/signup", json=data)

    assert response.status_code == 201
    assert response.json()["message"] == "Account created successfully"

def test_create_user_with_invalid_first_name(authorized_client):
    data = {
        "first_name": "Adam12",
        "last_name": "Bill",
        "email": "adam@gmail.com",
        "password": "password",
        "role": "admin"
    }

    response = authorized_client.post("/user/signup", json=data)

    assert response.status_code == 406
    assert response.json()["detail"] == "Invalid First Name"

def test_create_user_with_invalid_email(authorized_client):
    data = {
        "first_name": "Adam",
        "last_name": "Bill",
        "email": "adamgmail.com",
        "password": "password",
        "role": "admin"
    }

    response = authorized_client.post("/user/signup", json=data)

    assert response.status_code == 406
    assert response.json()["detail"] == "Invalid Email Address"

def test_create_user_with_invalid_password(authorized_client):
    data = {
        "first_name": "Adam",
        "last_name": "Bill",
        "email": "adam@mail.ubc.ca",
        "password": "pass",
        "role": "admin"
    }

    response = authorized_client.post("/user/signup", json=data)

    assert response.status_code == 406
    assert response.json()["detail"] == "Password must be at least 6 characters long"

def test_create_user_with_already_existing_email(authorized_client, test_verified_user):
    data = {
        "first_name": "Adam",
        "last_name": "Bill",
        "email": "teacher@gmail.com",
        "password": "password",
        "role": "admin"
    }

    response = authorized_client.post("/user/signup", json=data)

    assert response.status_code == 409
    assert response.json()["detail"] == "Account with this email already exists"

def test_create_user_with_invalid_jsonl(authorized_client, test_verified_user):
    data = {
        "first_name": "Adam",
        "last_name": "Bill",
        "email": "teacher@gmail.com",
        "password": "password",
        "role": "professor"
    }

    response = authorized_client.post("/user/signup", json=data)

    assert response.status_code == 422