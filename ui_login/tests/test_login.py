"""UI-автотесты страницы логина (ЛР №3): Selenium WebDriver + pytest."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

VALID_USER = "student"
VALID_PASSWORD = "Test123!"


def wait_visible(driver, locator, timeout=5):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def login(driver, username, password):
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()


def test_login_page_opens(driver, base_url):
    driver.get(base_url)
    assert "Вход" in driver.title
    assert driver.find_element(By.ID, "username").is_displayed()
    assert driver.find_element(By.ID, "password").is_displayed()


def test_login_with_valid_credentials(driver, base_url, shot):
    driver.get(base_url)
    shot("before")
    login(driver, VALID_USER, VALID_PASSWORD)

    logout = wait_visible(driver, (By.ID, "logout-btn"))  # кнопка «Logout» — признак успешного входа
    assert logout.text == "Logout"
    assert driver.find_element(By.ID, "welcome-name").text == VALID_USER
    shot("after")


def test_login_with_wrong_password_shows_error(driver, base_url, shot):
    driver.get(base_url)
    login(driver, VALID_USER, "wrong-password")

    error = wait_visible(driver, (By.ID, "error-message"))
    assert error.text == "Неверное имя пользователя или пароль"
    assert not driver.find_elements(By.ID, "logout-btn") or not driver.find_element(By.ID, "logout-btn").is_displayed()
    shot("error")
