from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 20)

    # Locators
    buy_tab = (By.ID, "inPageSearchForm_0")

    buy_tab_by_text = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='Buy']"
    )

    rent_tab = (By.ID, "inPageSearchForm_1")

    rent_tab_by_text = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and normalize-space()='Rent']"
    )

    search_box = (By.ID, "keyword2")

    search_button = (By.ID, "searchform_search_btn")

    search_button_by_text = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )

    def find_fresh_element(self, locators):

        if (
            isinstance(locators, tuple)
            and len(locators) == 2
            and isinstance(locators[0], str)
        ):
            locators = (locators,)

        last_error = None

        for locator in locators:
            try:
                return self.wait.until(
                    EC.presence_of_element_located(
                        locator
                    )
                )

            except TimeoutException as error:
                last_error = error

        raise last_error

    def click_when_ready(self, locators):

        last_error = None

        for _ in range(5):
            try:
                element = self.find_fresh_element(
                    locators
                )

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center'
                    });
                    """,
                    element
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                return

            except StaleElementReferenceException as error:
                last_error = error

        raise last_error

    # Actions
    def click_buy_tab(self):

        self.click_when_ready(
            (
                self.buy_tab,
                self.buy_tab_by_text
            )
        )


    def click_rent_tab(self):

        self.click_when_ready(
            (
                self.rent_tab,
                self.rent_tab_by_text
            )
        )

    def enter_location(self, location):

        last_error = None

        for _ in range(5):
            try:
                search = self.wait.until(
                    EC.visibility_of_element_located(
                        self.search_box
                    )
                )

                search.click()

                search.clear()

                search.send_keys(location)

                return

            except StaleElementReferenceException as error:
                last_error = error
                continue

        raise last_error

    def click_search(self):

        self.click_when_ready(
            (
                self.search_button,
                self.search_button_by_text
            )
        )
