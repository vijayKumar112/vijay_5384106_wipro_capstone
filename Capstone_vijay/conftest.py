import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from utilities.screenshot_helper import take_screenshot
from utilities.config_reader import (
    get_base_url,
    get_browser,
    get_implicit_wait
)


@pytest.fixture(scope="function")
def driver():

    browser = get_browser()

    if browser == "chrome":

        chrome_options = Options()

        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"]
        )

        chrome_options.add_experimental_option(
            "useAutomationExtension",
            False
        )
        driver = webdriver.Chrome(
            service=Service(),options=chrome_options
        )

        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )


    elif browser == "edge":

        driver = webdriver.Edge()

    else:
        raise Exception("Browser not supported")

    driver.maximize_window()

    driver.implicitly_wait(get_implicit_wait())

    driver.get(get_base_url())

    yield driver

    driver.quit()


@pytest.fixture
def screenshot(driver, request):

    def _capture(step_name):

        return take_screenshot(
            driver,
            request.node.name,
            step_name
        )

    return _capture


# Screenshot attachment for Allure report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call":

        driver = item.funcargs.get("driver", None)

        if driver:
            status = "passed" if report.passed else "failed"

            take_screenshot(
                driver,
                item.name,
                status
            )
