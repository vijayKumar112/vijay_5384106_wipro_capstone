from pages.filters_page import FiltersPage
from pages.home_page import HomePage
from pages.property_details_page import PropertyDetailsPage
from pages.search_results_page import SearchResultsPage
from utilities.logger import LogGen


logger = LogGen.loggen()
BUY_LOCATION = "Hyderabad"


def open_buy_results(driver):

    home = HomePage(driver)

    logger.info("Clicking Buy Tab")
    home.click_buy_tab()

    logger.info(f"Entering Location: {BUY_LOCATION}")
    home.enter_location(BUY_LOCATION)

    logger.info("Clicking Search Button")
    home.click_search()

    results_page = SearchResultsPage(driver)

    logger.info("Verifying Buy Search Results")
    assert results_page.verify_search_results()
    assert results_page.verify_buy_search_results()

    return results_page


def apply_core_buy_filters(driver):

    filters = FiltersPage(driver)

    logger.info("Closing popups if displayed")
    filters.click_ok_understood()

    logger.info("Applying 2 BHK Filter")
    filters.apply_2_bhk_filter()

    logger.info("Applying Residential Apartment Filter")
    filters.apply_residential_apartment_filter()

    logger.info("Applying Ready To Move Filter")
    filters.apply_ready_to_move_filter()

    logger.info("Applying Owner Filter")
    filters.apply_owner_filter()

    logger.info("Applying Locality Filter")
    locality_applied = filters.apply_locality_filter()
    logger.info(f"Locality Filter Applied: {locality_applied}")

    logger.info("Applying RERA Approved Filter")
    rera_applied = filters.apply_rera_approved_filter()
    logger.info(f"RERA Approved Filter Applied: {rera_applied}")

    return filters


def open_first_buy_property(driver):

    filters = apply_core_buy_filters(driver)

    logger.info("Selecting First Filtered Buy Result")
    assert filters.select_first_result()

    logger.info(
        f"Opened Buy Property Page URL: {driver.current_url}"
    )

    assert filters.verify_property_detail_page_opened()

    property_page = PropertyDetailsPage(driver)

    logger.info("Switching To Buy Property Window")
    property_page.switch_to_property_window()

    return property_page
