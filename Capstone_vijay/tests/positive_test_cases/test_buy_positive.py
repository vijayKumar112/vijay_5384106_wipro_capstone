import allure

from tests.buy_module_steps import (
    BUY_LOCATION,
    apply_core_buy_filters,
    open_buy_results,
    open_first_buy_property
)
from utilities.logger import LogGen


logger = LogGen.loggen()


@allure.epic("Selenium with Python")
@allure.feature("99acres Buy Module")
@allure.parent_suite("99acres Buy Module Test Cases")
@allure.suite("Positive Test Cases")
@allure.story("Positive Test Case 1")
@allure.title("Verify user can search buy properties by valid location")
def test_buy_search_by_location(driver):

    print("Positive Test Case 1: Verify user can search buy properties by valid location")

    results_page = open_buy_results(driver)

    heading = results_page.get_results_heading()

    logger.info(f"Buy Results Heading: {heading}")

    assert BUY_LOCATION.lower() in heading.lower()


@allure.epic("Selenium with Python")
@allure.feature("99acres Buy Module")
@allure.parent_suite("99acres Buy Module Test Cases")
@allure.suite("Positive Test Cases")
@allure.story("Positive Test Case 2")
@allure.title("Verify buy search results count is displayed")
def test_buy_results_count_is_displayed(driver):

    print("Positive Test Case 2: Verify buy search results count is displayed")

    results_page = open_buy_results(driver)

    results_count = results_page.get_results_count()

    logger.info(f"Buy Results Count: {results_count}")

    print(
        "Buy Results Count:",
        results_count
    )

    assert results_count > 0


@allure.epic("Selenium with Python")
@allure.feature("99acres Buy Module")
@allure.parent_suite("99acres Buy Module Test Cases")
@allure.suite("Positive Test Cases")
@allure.story("Positive Test Case 3")
@allure.title("Verify user can apply buy property filters")
def test_buy_property_filters_show_results(driver):

    print("Positive Test Case 3: Verify user can apply buy property filters")

    open_buy_results(driver)

    filters = apply_core_buy_filters(driver)

    logger.info("Verifying Filtered Buy Results")
    assert filters.verify_filtered_results()

    filtered_results_count = filters.get_results_count()

    logger.info(
        f"Filtered Buy Results Count: {filtered_results_count}"
    )

    print(
        "Filtered Buy Results Count:",
        filtered_results_count
    )

    assert filtered_results_count > 0


@allure.epic("Selenium with Python")
@allure.feature("99acres Buy Module")
@allure.parent_suite("99acres Buy Module Test Cases")
@allure.suite("Positive Test Cases")
@allure.sub_suite("End To End Test Case")
@allure.story("Positive Test Case 4")
@allure.title("Verify user can open buy property details and contact owner")
def test_buy_property_details_and_contact(driver):

    print("End To End Positive Test Case 4: Open buy property details and contact owner")

    open_buy_results(driver)

    property_page = open_first_buy_property(driver)

    logger.info("Clicking Shortlist")
    property_page.click_shortlist()

    logger.info("Opening Owner Details")
    property_page.open_owner_details()

    logger.info("Clicking View Phone Number")
    property_page.click_view_phone_number()

    logger.info("Verifying Contact Section")
    assert property_page.verify_contact_section()

    property_title = property_page.get_property_title()
    sale_price = property_page.get_sale_price()

    logger.info(f"Buy Property Title: {property_title}")
    logger.info(f"Sale Price: {sale_price}")

    assert property_title
    assert sale_price
