from test.test_fixtures import *

def test_server_runs(authorized_client):
    res = authorized_client.get("/")
    assert res.status_code == 200