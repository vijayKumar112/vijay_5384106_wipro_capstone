from datetime import datetime

import allure
from selenium import webdriver

from config.config_reader import config
from utilities.bdd_logger import get_logger


def before_all(context):
    config.screenshot_dir.mkdir(exist_ok=True)
    config.log_dir.mkdir(exist_ok=True)
    context.logger = get_logger("99acres-buy")


def before_scenario(context, scenario):
    context.driver = None
    context.logger.info("Starting scenario: %s", scenario.name)
    context.driver = _create_driver()
    context.driver.implicitly_wait(5)
    context.driver.maximize_window()


def after_scenario(context, scenario):
    driver = getattr(context, "driver", None)

    if driver is not None:
        screenshot_path = _save_scenario_screenshot(driver, scenario)
        _attach_screenshot_to_allure(driver, scenario)

        if scenario.status == "failed":
            context.logger.error("Scenario failed. Screenshot: %s", screenshot_path)

        driver.quit()

    context.logger.info("Finished scenario: %s - %s", scenario.name, scenario.status)


def _save_scenario_screenshot(driver, scenario):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = scenario.name.replace(" ", "_").replace("/", "_")
    screenshot_path = config.screenshot_dir / f"{safe_name}_{scenario.status}_{timestamp}.png"
    driver.save_screenshot(str(screenshot_path))
    return screenshot_path


def _attach_screenshot_to_allure(driver, scenario):
    screenshot = driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name=f"{scenario.name} - {scenario.status}",
        attachment_type=allure.attachment_type.PNG,
    )


def _create_driver():
    browser = config.browser_name

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        _apply_chromium_options(options)
        return webdriver.Chrome(options=options)

    if browser == "edge":
        options = webdriver.EdgeOptions()
        _apply_chromium_options(options)
        return webdriver.Edge(options=options)

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if config.headless:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    raise ValueError(f"Unsupported browser: {browser}")


def _apply_chromium_options(options):
    if config.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
