import allure

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.property_details_page import PropertyDetailsPage
from pages.search_results_page import SearchResultsPage
from pages.filters_page import FiltersPage

from utilities.logger import LogGen
from utilities.excel_reader import get_test_data


logger = LogGen.loggen()

data = get_test_data()

@allure.feature("99acres Rent Module")
@allure.story("End-to-End Property Search")
def test_end_to_end_property_flow(driver):
    # # LOGIN FLOW
    # login = LoginPage(driver)
    #
    # logger.info("Hovering Profile Icon")
    # login.hover_profile_icon()
    #
    # logger.info("Clicking Login/Register")
    # login.click_login_register()
    #
    # logger.info("Entering Mobile Number")
    # login.enter_mobile_number(
    #     data["mobile_number"]
    # )
    #
    # logger.info("Clicking Continue")
    # login.click_continue()
    #
    # import time
    #
    # logger.info(
    #     "Waiting 30 seconds for manual OTP entry"
    # )
    #
    # time.sleep(30)
    #
    # logger.info(
    #     "Clicking Verify & Continue"
    # )
    #
    # login.click_verify_and_continue()
    #
    # logger.info("Login Successful")
    #
    # logger.info(
    #     "Waiting for overlay to disappear"
    # )
    #
    # login.wait_for_overlay_to_disappear()

    # PROPERTY SEARCH FLOW
    home = HomePage(driver)

    logger.info("Clicking Rent Tab")
    home.click_rent_tab()

    logger.info(
        f"Entering Location: {data['location']}"
    )

    home.enter_location(data["location"])

    logger.info("Clicking Search Button")
    home.click_search()

    # SEARCH RESULTS VALIDATION
    results_page = SearchResultsPage(driver)

    logger.info("Verifying Search Results")

    logger.info(
        "Waiting for Results Page"
    )

    assert results_page.verify_search_results()

    logger.info(
        f"Results Heading: "
        f"{results_page.get_results_heading()}"
    )

    results_count = results_page.get_results_count()

    logger.info(
        f"Results Count: {results_count}"
    )

    print(
        "Results Count:",
        results_count
    )

    # FILTERS FLOW
    filters = FiltersPage(driver)

    logger.info(
        "Clicking Ok Understood Popup"
    )

    filters.click_ok_understood()

    logger.info(
        "Applying 2 BHK Filter"
    )

    filters.apply_2_bhk_filter()

    logger.info(
        "Applying Locality Filter"
    )

    locality_applied = filters.apply_locality_filter()

    logger.info(
        f"Locality Filter Applied: {locality_applied}"
    )

    logger.info(
        "Applying Independent House Filter"
    )

    filters.apply_independent_house_filter()

    logger.info(
        "Applying Owner Filter"
    )

    filters.apply_owner_filter()

    logger.info(
        "Verifying Filtered Results"
    )

    assert filters.verify_filtered_results()

    filtered_results_count = filters.get_results_count()

    logger.info(
        f"Filtered Results Count: {filtered_results_count}"
    )

    print(
        "Filtered Results Count:",
        filtered_results_count
    )

    logger.info(
        "Selecting First Filtered Result"
    )

    assert filters.select_first_result()

    logger.info(
        f"Opened Property Page URL: {driver.current_url}"
    )

    assert filters.verify_property_detail_page_opened()

    # PROPERTY DETAILS PAGE
    property_page = PropertyDetailsPage(
        driver
    )

    logger.info(
        "Switching To Property Window"
    )

    property_page.switch_to_property_window()

    logger.info(
        "Clicking Shortlist"
    )

    property_page.click_shortlist()

    logger.info(
        "Opening Owner Details"
    )

    property_page.open_owner_details()

    logger.info(
        "Clicking View Phone Number"
    )

    property_page.click_view_phone_number()

    logger.info(
        "Verifying Contact Section"
    )

    assert property_page.verify_contact_section()

    logger.info(
        f"Property Title: "
        f"{property_page.get_property_title()}"
    )

    logger.info(
        f"Rent Amount: "
        f"{property_page.get_rent_amount()}"
    )
