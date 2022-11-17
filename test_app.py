import json
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"

# 1
def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"

#3
def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"

#2
def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19

#4
def test_post_users_success(client):
    data = {
        "name": "helena2",
        "age": 23,
        "team": "C2TC"
    }
    res = client.post(
        "/users",
        data = json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    assert res.status_code == 201

    res_users = res.json["result"]["newUser"]
    assert len(res_users) == 4
    assert res_users["name"] == "helena2"
    assert res_users["id"] == 5
    assert res_users["team"] == "C2TC"
    assert res_users["age"] == 23

def test_post_users_fail_name(client):
    data = {
        "age": 23,
        "team": "C2TC"
    }
    res = client.post(
        "/users",
        data = json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    assert res.status_code == 422

    res_message = res.json["message"]
    assert res_message == "missing name"

def test_post_users_fail_age(client):
    data = {
        "name": "helena2",
        "team": "C2TC"
    }
    res = client.post(
        "/users",
        data = json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    assert res.status_code == 422

    res_message = res.json["message"]
    assert res_message == "missing age"

def test_post_users_fail_team(client):
    data = {
        "name": "helena2",
        "age": 23
    }
    res = client.post(
        "/users",
        data = json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    assert res.status_code == 422

    res_message = res.json["message"]
    assert res_message == "missing team"

#5
def test_put_users_id_success(client):
    data = {
        "name": "helena2",
        "age": 23,
        "team": "C2TC"
    }
    res = client.put(
        "/users/1",
        data = json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    assert res.status_code == 201

    res_user = res.json["result"]["updatedUser"]
    assert len(res_user) == 4
    assert res_user["name"] == "helena2"
    assert res_user["id"] == 1
    assert res_user["team"] == "C2TC"
    assert res_user["age"] == 23

def test_put_users_id_fail(client):
    data = {
        "name": "helena2",
        "age": 23,
        "team": "C2TC"
    }
    res = client.put(
        "/users/6",
        data = json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    assert res.status_code == 404

    res_message = res.json["message"]
    assert res_message == "doesn't exist a user with the provided id"