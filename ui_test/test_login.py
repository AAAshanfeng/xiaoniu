from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login_uel = "http://ceshixiaoniu.com/ecommerce-practice-app.html"


def test_login_success(driver):

    driver.get(login_uel)

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

    logout_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "logoutBtn"))
    )

    assert logout_btn.is_displayed()


def test_wrong_username(driver):
    driver.get(login_uel)

    driver.find_element(By.ID, "username").send_keys("wrong_username")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "loginBtn").click()

    warning = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "toast"))
    )

    assert warning.text == "账号或密码错误"


def test_wrong_password(driver):
    driver.get(login_uel)

    driver.find_element(By.ID, "username").send_keys("tester")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "loginBtn").click()

    warning = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "toast"))
    )

    assert warning.text == "账号或密码错误"


def test_logout(login):
    driver = login

    logout_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logoutBtn"))
    )
    logout_btn.click()

    # 退出成功后，登录表单区的用户名输入框重新显示
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )

    assert username_input.is_displayed()
