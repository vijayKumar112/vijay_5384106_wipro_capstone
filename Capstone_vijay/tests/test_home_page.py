# from pages.home_page import HomePage
#
# from utilities.logger import LogGen
#
# logger = LogGen.loggen()
#
#
# def test_homepage_elements(driver):
#
#     logger.info("Starting homepage validation")
#
#     home = HomePage(driver)
#
#     assert driver.title is not None
#
#     assert home.wait.until(
#         lambda d: d.find_element(*home.buy_tab).is_displayed()
#     )
#
#     assert home.wait.until(
#         lambda d: d.find_element(*home.search_box).is_displayed()
#     )
#
#     assert home.wait.until(
#         lambda d: d.find_element(*home.search_button).is_displayed()
#     )
#
#     logger.info("Homepage elements validated successfully")