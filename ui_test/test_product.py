from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_product_list_display(login):
    driver = login

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-card"))
    )

    products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
    assert len(products) == 4

    card_003 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='products']/article[3]"))
    )
    assert "AI测试资料包" in card_003.text
    assert "¥99.00" in card_003.text

