import logging
import os

import allure
import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    driver=webdriver.Chrome()
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
