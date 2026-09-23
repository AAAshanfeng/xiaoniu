from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_checkout_flow(login):
    driver = login

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-add-cart='101']"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "toast"))
    )

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-add-cart='103']"))
    ).click()

    cart = WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, ".cart-item")) == 2
    )
    assert cart

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "createOrderBtn"))
    ).click()

    order = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".order-card"))
    )
    assert "待支付" in order.text
    assert "¥298.00" in order.text

    pay_btn = order.find_element(By.CSS_SELECTOR, "[data-pay-order]")
    order_id = pay_btn.get_attribute("data-pay-order")
    pay_btn.click()

    order_locator = (By.XPATH, f'//article[contains(@class, "order-card")][.//strong[contains(text(), "{order_id}")]]')

    WebDriverWait(driver, 10).until(
        lambda d: "已支付" in d.find_element(*order_locator).text
    )

    order = driver.find_element(*order_locator)
    assert "已支付" in order.text