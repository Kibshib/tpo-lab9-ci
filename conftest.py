"""Параметр запуска и фикстура с гарантированным закрытием браузера."""

import pytest

from browser import create_driver


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False,
                     help="Запустить Chrome без видимого окна")


@pytest.fixture
def driver(request):
    browser = create_driver(headless=request.config.getoption("--headless"))
    try:
        yield browser
    finally:
        browser.quit()
