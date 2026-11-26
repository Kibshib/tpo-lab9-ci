"""Chrome для локального запуска и GitHub Actions."""

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

LOGIN_URL = "https://the-internet.herokuapp.com/login"
ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def create_driver(headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,900")
    if headless:
        options.add_argument("--headless=new")
    if os.getenv("CI") == "true":
        options.add_argument("--disable-dev-shm-usage")
    cache = DriverCacheManager(root_dir=str(Path(__file__).resolve().parent))
    service = Service(ChromeDriverManager(cache_manager=cache).install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver
