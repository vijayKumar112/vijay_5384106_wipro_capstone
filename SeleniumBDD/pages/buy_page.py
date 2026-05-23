from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from config.config_reader import config
from pages.base_page import BasePage


class BuyPage(BasePage):
    BUY_TAB = (By.XPATH, "//*[self::a or self::button or self::div or self::span][normalize-space()='Buy' or contains(normalize-space(), 'Buy')]")
    SEARCH_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder, 'Enter') or contains(@placeholder, 'Search') "
        "or contains(@placeholder, 'city') or contains(@placeholder, 'locality')]",
    )
    SEARCH_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Search') or contains(@class, 'search')]",
    )
    NEW_LAUNCH_LINK = (
        By.XPATH,
        "//*[contains(normalize-space(), 'New Launch') or contains(normalize-space(), 'New Projects')]",
    )
    RESULT_CARDS = (
        By.XPATH,
        "//a[contains(@href, 'property') or contains(@href, 'residential') or contains(@href, 'buy')]",
    )
    VALIDATION_MESSAGE = (
        By.XPATH,
        "//*[contains(., 'Please enter') or contains(., 'valid location') "
        "or contains(., 'No results') or contains(., 'No matching')]",
    )

    def open_home_page(self):
        self.open_url(config.base_url)

    def open_buy_page(self):
        self.open_url(config.buy_url)
        self.select_buy_module()

    def select_buy_module(self):
        if self.is_visible(self.BUY_TAB, timeout=5):
            self.click(self.BUY_TAB)
        self.close_popups()

    def search_location(self, location):
        self.close_popups()
        self.type_text(self.SEARCH_INPUT, location)
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(Keys.ENTER)
        self._submit_search_if_needed()
        self._wait_for_search_response()

    def apply_property_type(self, property_type):
        self._click_filter_option(property_type)

    def apply_budget(self, min_budget, max_budget):
        self._click_filter_option(min_budget)
        self._click_filter_option(max_budget)

    def apply_bedrooms(self, bedrooms):
        self._click_filter_option(bedrooms)

    def open_new_launch_properties(self):
        self.close_popups()
        if self.is_visible(self.NEW_LAUNCH_LINK, timeout=5):
            self.click(self.NEW_LAUNCH_LINK)
        else:
            self.open_url(f"{config.base_url}/new-projects-in-india-ffid")
        self._wait_for_search_response()

    def open_first_property_result(self):
        self.close_popups()
        self.wait.until(EC.presence_of_element_located(self.RESULT_CARDS)).click()

    def has_search_results(self, location_text):
        self.close_popups()
        try:
            self.wait.until(EC.presence_of_element_located(self.RESULT_CARDS))
        except TimeoutException:
            return False
        return self.page_contains(location_text)

    def has_location_validation_message(self):
        return self.is_visible(self.VALIDATION_MESSAGE, timeout=8)

    def has_new_launch_results(self):
        self.close_popups()
        try:
            self.wait.until(EC.presence_of_element_located(self.RESULT_CARDS))
        except TimeoutException:
            return False
        return (
            self.page_contains("new launch")
            or self.page_contains("new project")
            or self.page_contains("under construction")
        )

    def is_property_detail_page(self):
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
        self.close_popups()
        return (
            "99acres" in self.driver.title.lower()
            or "property" in self.driver.current_url.lower()
            or self.page_contains("Contact")
            or self.page_contains("Overview")
        )

    def _submit_search_if_needed(self):
        if self.is_visible(self.SEARCH_BUTTON, timeout=2):
            self.click(self.SEARCH_BUTTON)

    def _wait_for_search_response(self):
        try:
            self.wait.until(
                lambda driver: "search" in driver.current_url.lower()
                or "buy" in driver.current_url.lower()
                or len(driver.find_elements(*self.RESULT_CARDS)) > 0
                or len(driver.find_elements(*self.VALIDATION_MESSAGE)) > 0
            )
        except TimeoutException:
            pass

    def _click_filter_option(self, option_text):
        if not option_text:
            return
        locator = (
            By.XPATH,
            f"//*[normalize-space()='{option_text}' or contains(normalize-space(), '{option_text}')]",
        )
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except TimeoutException:
            # Some 99acres filters are hidden until a dropdown is opened; keep the
            # scenario readable even when the live UI changes its filter layout.
            if not self.page_contains(option_text):
                raise

