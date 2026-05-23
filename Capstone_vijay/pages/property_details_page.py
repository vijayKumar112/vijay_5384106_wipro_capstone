import re

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utilities.config_reader import get_implicit_wait


class PropertyDetailsPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 40)

    # =========================
    # POPUPS
    # =========================

    ok_understood_button = (
        By.XPATH,
        "//*[self::button or self::div or self::span]"
        "[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'understood')]"
    )

    cookie_ok_button = (
        By.XPATH,
        "//*["
        "(self::button or self::div or self::span)"
        " and (normalize-space()='Okay' or normalize-space()='OK')"
        "] | //button["
        "contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'accept') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'agree')]"
    )

    # =========================
    # LOCATORS
    # =========================

    shortlist_button = (
        By.ID,
        "shortListBtn"
    )

    owner_details_tab = (
        By.XPATH,
        "//*[self::button or self::div or self::span or self::a]"
        "[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'owner details')]"
    )

    view_phone_button = (
        By.XPATH,
        "//*[@id='OwnerDetails']/div/input"

    )

    contact_section = (
        By.XPATH,
        "//*[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'contact') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'phone') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'login') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'register')]"
    )

    property_title = (
        By.XPATH,
        "//h1 | "
        "//*[self::h2 or self::h3 or self::div or self::span]"
        "[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'independent house/villa for rent') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'for sale') "
        "or contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'flat in')]"
    )

    # =========================
    # COMMON METHODS
    # =========================

    def click_visible_if_present(self, locator, timeout=3):

        self.driver.implicitly_wait(0)

        try:
            elements = WebDriverWait(
                self.driver,
                timeout
            ).until(
                EC.visibility_of_any_elements_located(
                    locator
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                elements[0]
            )

            return True

        except (StaleElementReferenceException, TimeoutException):
            return False

        finally:
            self.driver.implicitly_wait(
                get_implicit_wait()
            )

    def handle_blocking_popups(self):

        clicked = False

        for _ in range(3):
            clicked_this_round = (
                self.click_visible_if_present(
                    self.ok_understood_button
                )
                or self.click_visible_if_present(
                    self.cookie_ok_button
                )
            )

            clicked = clicked or clicked_this_round

            if not clicked_this_round:
                break

        return clicked

    def find_visible_element(self, locator, max_scrolls=8, timeout=10):

        self.driver.implicitly_wait(0)

        try:
            for _ in range(max_scrolls):

                elements = self.driver.find_elements(
                    *locator
                )

                for element in elements:
                    try:
                        if element.is_displayed():
                            return element

                    except StaleElementReferenceException:
                        continue

                self.driver.execute_script(
                    "window.scrollBy(0, Math.floor(window.innerHeight * 0.55));"
                )

            return WebDriverWait(
                self.driver,
                timeout
            ).until(
                EC.visibility_of_element_located(
                    locator
                )
            )

        finally:
            self.driver.implicitly_wait(
                get_implicit_wait()
            )

    def scroll_to_and_click(self, element):

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

    def click_detail_page_element(self, locator, max_scrolls=8):

        self.handle_blocking_popups()

        element = self.find_visible_element(
            locator,
            max_scrolls=max_scrolls
        )

        self.scroll_to_and_click(
            element
        )

        self.handle_blocking_popups()

        return True

    # =========================
    # ACTIONS
    # =========================

    def switch_to_property_window(self):

        all_windows = self.driver.window_handles

        self.driver.switch_to.window(
            all_windows[-1]
        )

        self.wait.until(
            lambda driver: driver.current_url
            and driver.current_url != "about:blank"
        )

        self.handle_blocking_popups()

    def click_shortlist(self):

        return self.click_detail_page_element(
            self.shortlist_button,
            max_scrolls=3
        )

    def open_owner_details(self):

        return self.click_detail_page_element(
            self.owner_details_tab,
            max_scrolls=6
        )

    def click_view_phone_number(self):

        return self.click_detail_page_element(
            self.view_phone_button,
            max_scrolls=8
        )

    # =========================
    # VALIDATIONS
    # =========================

    def get_property_title(self):

        title_element = self.find_visible_element(
            self.property_title,
            max_scrolls=1,
            timeout=5
        )

        title = title_element.text.strip()

        if title:
            return title

        return self.extract_title_from_body()

    def get_rent_amount(self):

        body_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        match = re.search(
            r"(?:₹|Rs\.?\s?)([\d,]+)",
            body_text
        )

        if match:
            return match.group(0)

        raise TimeoutException(
            "Rent amount was not found on the property details page"
        )

    def get_sale_price(self):

        body_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        price_patterns = (
            r"(?:\u20b9|Rs\.?\s?)\s?[\d,.]+\s?(?:Cr|Crore|Lac|Lakh)",
            r"(?:\u20b9|Rs\.?\s?)\s?[\d,]+"
        )

        for pattern in price_patterns:
            match = re.search(
                pattern,
                body_text,
                re.IGNORECASE
            )

            if match and "/month" not in match.group(0).lower():
                return match.group(0)

        raise TimeoutException(
            "Sale price was not found on the property details page"
        )

    def extract_title_from_body(self):

        body_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        for line in body_text.splitlines():
            normalized_line = line.strip()

            if "for Rent" in normalized_line or "for Sale" in normalized_line:
                return normalized_line

        return body_text.splitlines()[0].strip()

    def verify_contact_section(self):

        element = self.find_visible_element(
            self.contact_section,
            max_scrolls=5,
            timeout=10
        )

        return element.is_displayed()
