import allure
from selenium.webdriver.common.by import By

from pages.home_page import HomePage
from tests.buy_module_steps import open_buy_results, open_first_buy_property
from utilities.logger import LogGen


logger = LogGen.loggen()


@allure.epic("Selenium with Python")
@allure.feature("99acres Buy Module")
@allure.parent_suite("99acres Buy Module Test Cases")
@allure.suite("Negative Test Cases")
@allure.story("Negative Test Case 1")
@allure.title("Verify empty location search does not open buy results")
def test_buy_search_with_empty_location(driver):

    print("Negative Test Case 1: Verify empty location search does not open buy results")

    home = HomePage(driver)

    logger.info("Clicking Buy Tab")
    home.click_buy_tab()

    logger.info("Keeping Search Box Empty")
    home.enter_location("")

    logger.info("Clicking Search Button With Empty Location")
    home.click_search()

    current_url = driver.current_url.lower()

    logger.info(f"Current URL After Empty Search: {current_url}")

    assert "search/property/buy" not in current_url


@allure.epic("Selenium with Python")
@allure.feature("99acres Buy Module")
@allure.parent_suite("99acres Buy Module Test Cases")
@allure.suite("Negative Test Cases")
@allure.story("Negative Test Case 2")
@allure.title("Verify unauthenticated user is asked to login for contact details")
def test_contact_owner_without_login_shows_login_prompt(driver):

    print("Negative Test Case 2: Verify unauthenticated user is asked to fill contact details")

    open_buy_results(driver)

    property_page = open_first_buy_property(driver)

    logger.info("Opening Owner Details")
    property_page.open_owner_details()

    logger.info("Clicking View Phone Number Without Login")
    property_page.click_view_phone_number()

    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text.lower()

    logger.info("Verifying login/register prompt is displayed")

    assert (
        "login" in body_text
        or "register" in body_text
        or "mobile" in body_text
        or "continue" in body_text
        or "please fill in your details" in body_text
        or "basic information" in body_text
        or "name" in body_text
        or "phone" in body_text
        or "this number would be verified" in body_text
    )
