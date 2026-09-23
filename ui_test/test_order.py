from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# pytest ui_test -v --html=report/ui_report.html --self-contained-html


def test_create_order(login):
    driver = login

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-add-cart="103"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "createOrderBtn"))
    ).click()

    order = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".order-card"))
    )

    assert "待支付" in order.text
    assert "¥99.00" in order.text
    assert "AI测试资料包 × 1" in order.text


def test_pay_order(login):
    driver = login

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-add-cart="103"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "createOrderBtn"))
    ).click()

    order = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".order-card"))
    )

    assert "待支付" in order.text

    pay_btn = order.find_element(By.CSS_SELECTOR, "[data-pay-order]")

    order_id = pay_btn.get_attribute("data-pay-order")

    pay_btn.click()

    order_locator = (By.XPATH, f'//article[contains(@class, "order-card")][.//strong[contains(text(), "{order_id}")]]')

    # 等待订单状态变成“已支付”
    WebDriverWait(driver, 10).until(
        lambda d: "已支付" in d.find_element(*order_locator).text
    )

    # 再重新获取订单
    order = driver.find_element(*order_locator)

    assert "已支付" in order.text


def test_cancel_order(login):
    driver = login

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-add-cart="103"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "createOrderBtn"))
    ).click()

    order = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".order-card"))
    )

    assert "待支付" in order.text

    # 只在order里面找元素
    pay_btn = order.find_element(By.CSS_SELECTOR, "[data-cancel-order]")

    order_id = pay_btn.get_attribute("data-cancel-order")

    pay_btn.click()

    order_locator = (By.XPATH, f'//article[contains(@class, "order-card")][.//strong[contains(text(), "{order_id}")]]')

    WebDriverWait(driver, 10).until(
        lambda d: "已取消" in d.find_element(*order_locator).text
    )

    order = driver.find_element(*order_locator)

    assert "已取消" in order.text


def test_create_order_empty_cart(login):
    driver = login

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "createOrderBtn"))
    ).click()

    warning = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "toast").text == "购物车为空，不能创建订单"
    )

    assert warning
    assert len(driver.find_elements(By.CSS_SELECTOR, ".order-card")) == 0