from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_add_cart(login):
    driver = login

    add_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-add-cart="101"]'))
    )
    add_cart_btn.click()

    cart_item = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-remove-cart="101"]' ))
    )

    assert cart_item.is_displayed()


def test_delete_cart(login):
    driver = login

    add_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-add-cart="101"]'))
    )
    add_cart_btn.click()

    delete_cart_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-remove-cart="101"]'))
    )
    delete_cart_btn.click()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, '[data-remove-cart="101"]'))
    )


def test_repeat_add_cart(login):
    driver = login

    add_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-add-cart="101"]'))
    )
    add_cart_btn.click()

    add_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-add-cart="101"]'))
    )
    add_cart_btn.click()

    cart_item = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.cart-item'))
    )

    assert "数量：2 " in cart_item.text
    assert "¥398.00" in cart_item.text


def test_out_of_stock_button_disabled(login):
    driver = login

    add_cart_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-add-cart="104"]'))
    )
    assert not add_cart_btn.is_enabled()