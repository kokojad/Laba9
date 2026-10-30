"""Базовый класс Page Object: общие действия над страницей с явными ожиданиями."""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str, timeout: float = 5):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

    # --- навигация ---
    def open(self, path: str = ""):
        self.driver.get(self.base_url + path)
        return self

    @property
    def title(self) -> str:
        return self.driver.title

    # --- поиск и ожидания ---
    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, self.timeout if timeout is None else timeout)

    def find(self, locator):
        return self._wait().until(EC.presence_of_element_located(locator))

    def wait_visible(self, locator, timeout=None):
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def is_visible(self, locator) -> bool:
        elements = self.driver.find_elements(*locator)
        return bool(elements) and elements[0].is_displayed()

    # --- действия ---
    def click(self, locator):
        self._wait().until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str):
        element = self.wait_visible(locator)
        element.clear()
        if text:
            element.send_keys(text)

    def select_by_value(self, locator, value: str):
        Select(self.wait_visible(locator)).select_by_value(value)

    def set_checkbox(self, locator, checked: bool):
        element = self.wait_visible(locator)
        if element.is_selected() != checked:
            element.click()

    def text_of(self, locator) -> str:
        return self.find(locator).text

    def value_of(self, locator) -> str:
        return self.find(locator).get_attribute("value")
