from test.test_fixtures import *

def test_edit_user(authorized_client, test_verified_admin_1):
    img_path = "assets/test.png"

    data = {
        "email": "admin1@korse.com",
        "password": "password",
        "bio": "Updated Bio",
        "gender": "male",
        "pronouns": "he/his/him",
        "contact": "+12345678768",
        "office": "Room 333, SCI",
        "department": None,
        "year": None,
        "degree": None,
        "faculty": None,
    }

    response = authorized_client.patch("/user/edit", data=data, files={'profile_image': ("course_img.png", open(img_path, "rb"))})
    assert response.status_code == 200
    assert response.json()["message"] == "User Profile Updated Successfully"

    res2 = authorized_client.post("/user/get_user",json={'email': 'admin1@korse.com', 'password': 'password'})
    assert res2.json()["user"]["bio"] == "Updated Bio"
    assert res2.json()["office"] == "Room 333, SCI"
