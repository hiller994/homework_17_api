import json

import pytest
import requests
from jsonschema import validate

from homework_17.data.file_path import path

@pytest.fixture(scope='function')
def create_user_for_edit():
    response = requests.post("https://reqres.in/api/users", data={
        "name": "Andreyforedit",
        "job": "tester"
    })
    body = response.json()
    id_user_for_edit = body["id"]
    yield id_user_for_edit

@pytest.fixture(scope='function')
def create_user_for_delete():
    response = requests.post("https://reqres.in/api/users", data={
        "name": "Andreyfordelete",
        "job": "tester"
    })
    body = response.json()
    id_user_for_delete = body["id"]
    yield id_user_for_delete

def test_get_view_list_users():
    response = requests.get(
        "https://reqres.in/api/users",
        params= {"page" : 2}
    )
    body = response.json()  # тело ответа
    assert response.status_code == 200

    schema_path = path("get_list_users.json")
    with open(schema_path) as file:
        validate(body, schema=json.loads(file.read()))



def test_post_create_user():
    response = requests.post("https://reqres.in/api/users", data={
        "name": "morpheus",
        "job": "leader"
    })
    body = response.json()

    assert response.status_code == 201

    with open(path("post_users.json")) as file:
        validate(body, schema=json.loads(file.read()))



def test_put_editing_user(create_user_for_edit):
    job = "tester"
    name = "Andrey"

    response = requests.put(f"https://reqres.in/api/users/{create_user_for_edit}", data={
        "name": name,
        "job": job
    })
    body = response.json()

    assert body["name"] == name
    assert body["job"] == job
    with open(path("put_users.json")) as file:
        validate(body, schema=json.loads(file.read()))



def test_delete_user(create_user_for_delete):

    response = requests.delete(f"https://reqres.in/api/users/{create_user_for_delete}")
    assert response.status_code == 204

def test_get_user_not_found():
    user_id = "1234"

    response = requests.get(f"https://reqres.in/api/users/{user_id}")
    assert response.status_code == 404

def test_post_registration_user():
    response = requests.post("https://reqres.in/api/register", data={
    "email": "eve.holt@reqres.in",
    "password": "pistol"
    })
    body = response.json()

    assert response.status_code == 200
    assert response.json()['token'] is not None

    with open(path("post_users_reg.json")) as file:
        validate(body, schema=json.loads(file.read()))

def test_post_authorization_not_login():
    response = requests.post("https://reqres.in/api/login", data={
        "email": "",
        "password": ""
    })

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing email or username'

