import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from stand_server import start_server

SCREENSHOTS = Path(__file__).resolve().parent.parent / "screenshots"


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="запускать Chrome с окном (по умолчанию headless)")


@pytest.fixture(scope="session")
def base_url():
    server, url = start_server()
    yield url
    server.shutdown()


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    headless = not request.config.getoption("--headed") and os.environ.get("HEADLESS", "1") != "0"
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1100,800")
    options.add_argument("--lang=ru")
    if os.environ.get("CI"):  # GitHub Actions выставляет переменную CI=true
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    # chromedriver скачивается и кэшируется библиотекой webdriver-manager
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(0)  # используем только явные ожидания
    yield drv
    drv.quit()


@pytest.fixture
def shot(driver, request):
    """Сохраняет скриншот в screenshots/<имя_теста>_<метка>.png."""
    SCREENSHOTS.mkdir(exist_ok=True)

    def _shot(label):
        path = SCREENSHOTS / f"{request.node.name}_{label}.png"
        driver.save_screenshot(str(path))
        return path

    return _shot
