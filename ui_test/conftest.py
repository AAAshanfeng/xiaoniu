import pytest
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_url = "http://43.133.227.52/api"
UI_url = "http://ceshixiaoniu.com/ecommerce-practice-app.html"


@pytest.fixture()
def driver():
    driver = webdriver.Edge()
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture()
def reset_data():
    login_response = requests.post(
        f"{BASE_url}/login",
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
        f"{BASE_url}/reset",
        headers=header
    )
    assert reset_response.status_code == 200


@pytest.fixture()
def login(driver, reset_data):
    driver.get(UI_url)

    username = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    username.clear()
    username.send_keys("tester")

    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password.clear()
    password.send_keys("123456")

    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "loginBtn"))
    )
    login_btn.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "logoutBtn"))
    )

    return driver