import requests
import pytest
from .api_client import ApiClient

base_url = "http://43.133.227.52/api"

"""
@pytest.fixture(scope="module")
def login(username, password):
    login_response = requests.post(f"{base_url}/login", json={
        "username": "tester",
        "password": "123456"
    })

    assert login_response.status_code == 200

    token = login_response.json()["token"]

    return {
        "Authorization": f"Bearer {token}"
    }
"""


# 提供公共对象
@pytest.fixture(scope="session")
def api():
    return ApiClient(base_url)


@pytest.fixture()
def reset_data():
    login_response = requests.post(
        f"{base_url}/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    assert login_response.status_code == 200

    token = login_response.json()["token"]

    header = {
        "Authorization": f"Bearer {token}"
    }

    reset_response = requests.post(
        f"{base_url}/reset",
        headers=header
    )
    assert reset_response.status_code == 200


@pytest.fixture()
def login(reset_data):
    def _login(username, password):
        response = requests.post(f"{base_url}/login", json={
            "username": username,
            "password": password
        })

        assert response.status_code == 200

        token = response.json()["token"]

        return {
            "Authorization": f"Bearer {token}"
        }
    return _login


@pytest.fixture()
def user_header(login):
    return login("tester", "123456")


@pytest.fixture()
def admin_header(login):
    return login("admin", "admin123")