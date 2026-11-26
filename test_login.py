"""Пункт 3 задания: успешный вход с опубликованной учебной учётной записью."""

from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser import ARTIFACTS, LOGIN_URL


def test_valid_login(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 10)

    username = wait.until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    username.send_keys("tomsmith")
    driver.find_element(By.NAME, "password").send_keys("SuperSecretPassword!")
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '#login button[type="submit"]')
    )).click()

    wait.until(EC.url_to_be("https://the-internet.herokuapp.com/secure"))
    logout = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'a[href="/logout"]')
    ))
    flash = wait.until(EC.visibility_of_element_located((By.ID, "flash")))

    assert urlparse(driver.current_url).path == "/secure"
    assert logout.is_displayed()
    assert logout.text.strip() == "Logout"
    assert "You logged into a secure area!" in flash.text

    ARTIFACTS.mkdir(exist_ok=True)
    driver.save_screenshot(str(ARTIFACTS / "successful_login.png"))
