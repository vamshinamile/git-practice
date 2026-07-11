import logging
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def driver(request):

    options = Options()

    # If running on GitHub Actions
    if os.getenv("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=options)
    

    driver.maximize_window()
    driver.get("https://www.amazon.in/")

    request.node.driver = driver

    yield driver

    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        # Flush all log handlers
        for handler in logging.getLogger().handlers:
            handler.flush()

        driver = getattr(item, "driver", None)

        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
