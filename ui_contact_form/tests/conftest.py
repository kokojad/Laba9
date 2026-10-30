import os
from pathlib import Path

import pytest
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.contact_page import ContactPage
from stand_server import start_server

SCREENSHOTS = Path(__file__).resolve().parent.parent / "screenshots"


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="запускать Chrome с окном (по умолчанию headless)")


@pytest.fixture(scope="session")
def base_url():
    server, url = start_server()
    yield url
    server.shutdown()


@pytest.fixture(scope="module")
def driver(request):
    options = webdriver.ChromeOptions()
    if not request.config.getoption("--headed") and os.environ.get("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1100,950")
    options.add_argument("--lang=ru")
    if os.environ.get("CI"):  # GitHub Actions выставляет переменную CI=true
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    drv.implicitly_wait(0)
    yield drv
    drv.quit()


@pytest.fixture
def contact_page(driver, base_url):
    """Страница обратной связи, открытая «с нуля» для каждого теста."""
    return ContactPage(driver, base_url).open_page()


@pytest.fixture
def shot(driver, request):
    SCREENSHOTS.mkdir(exist_ok=True)

    def _shot(label):
        path = SCREENSHOTS / f"{label}.png"
        driver.save_screenshot(str(path))
        # обрезаем пустое пространство под карточкой формы
        bottom = int(driver.execute_script(
            "return document.querySelector('.card').getBoundingClientRect().bottom") + 24)
        img = Image.open(path)
        img.crop((0, 0, img.width, min(bottom, img.height))).save(path)
        return path

    return _shot
