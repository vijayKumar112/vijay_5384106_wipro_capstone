import re

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchResultsPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 40)

    # =========================
    # LOCATORS
    # =========================

    # Results Heading
    results_heading = (
        By.TAG_NAME,
        "h1"
    )

    # Property Cards
    property_cards = (
        By.CSS_SELECTOR,
        "div[data-label='SEARCH']"
    )

    result_count_text = (
        By.XPATH,
        "//*[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'results')]"
    )

    # =========================
    # ACTIONS
    # =========================

    def wait_for_results_page(self):

        self.wait.until(
            EC.url_contains("property")
        )

    def verify_search_results(self):

        self.wait_for_results_page()

        heading = self.wait.until(
            EC.visibility_of_element_located(
                self.results_heading
            )
        )

        print("Results Heading:", heading.text)

        return heading.is_displayed()

    def get_results_heading(self):

        heading = self.wait.until(
            EC.visibility_of_element_located(
                self.results_heading
            )
        )

        return heading.text

    def verify_buy_search_results(self):

        heading = self.get_results_heading()

        return (
            "sale" in heading.lower()
            or "/buy/" in self.driver.current_url.lower()
            or "preference=s" in self.driver.current_url.lower()
        )

    def verify_rent_search_results(self):

        heading = self.get_results_heading()

        return (
            "rent" in heading.lower()
            or "/rent/" in self.driver.current_url.lower()
            or "preference=r" in self.driver.current_url.lower()
        )

    def get_results_count(self):

        count = self.get_results_count_from_visible_text()

        if count is not None:
            return count

        results = self.driver.find_elements(
            *self.property_cards
        )

        return len(results)

    def get_results_count_from_visible_text(self):

        try:
            return WebDriverWait(
                self.driver,
                10
            ).until(
                lambda driver: self.extract_results_count()
            )

        except TimeoutException:
            return None

    def extract_results_count(self):

        candidates = [
            self.get_results_heading()
        ]

        elements = self.driver.find_elements(
            *self.result_count_text
        )

        for element in elements:
            try:
                if element.is_displayed():
                    candidates.append(
                        element.text
                    )

            except Exception:
                continue

        for text in candidates:
            match = re.search(
                r"([\d,]+)\s+results?",
                text,
                re.IGNORECASE
            )

            if match:
                return int(
                    match.group(1).replace(",", "")
                )

        return False
