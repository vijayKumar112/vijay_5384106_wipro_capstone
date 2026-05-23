import re

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.config_reader import get_implicit_wait


class FiltersPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 40)

    # =========================
    # POPUP
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
    # FILTER LOCATORS
    # =========================

    # 2 BHK Filter
    bhk_2_filter = (
        By.XPATH,
        "//*[@id='2']"
    )


    # Type of Property Section
    property_type_section = (
        By.ID,
        "property_type"
    )

    # Independent House / Villa Option
    independent_house_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (self::label or self::div or self::span) "
        "and contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'independent house')]"
    )

    residential_apartment_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (self::label or self::div or self::span) "
        "and contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'residential apartment')]"
    )

    ready_to_move_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (self::label or self::div or self::span or self::button) "
        "and contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'ready to move')]"
    )

    rera_approved_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (self::label or self::div or self::span or self::button) "
        "and contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'rera approved')]"
    )

    # Owner quick filter
    owner_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and not(ancestor::*[@data-cnstrc-item-name='propertyTuple']) "
        "and (self::button or self::div or self::span or self::label) "
        "and normalize-space()='Owner']"
    )

    # Locality filters are loaded dynamically, so prefer a known locality
    # when it is visible and otherwise select the first available option.
    hitech_city_filter = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and (self::label or self::div or self::span) "
        "and contains(normalize-space(),'Hitech City')]"
    )

    locality_filter_options = (
        By.XPATH,
        "//label[contains("
        "translate(@for,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'locality') "
        "and not(contains("
        "translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'disabled'))]"
    )

    locality_section = (
        By.XPATH,
        "//*[not(ancestor::*[@data-label='SEARCH']) "
        "and contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'locality')]"
    )

    loading_placeholder = (
        By.CSS_SELECTOR,
        ".pageComponent.loadingPlaceholder, "
        "[class*='loadingPlaceholder']"
    )

    property_title_inside_card = (
        By.CSS_SELECTOR,
        "a, h2, h3, [class*='title'], [class*='project'], "
        "[class*='tuple'], [class*='srpTuple']"
    )

    property_link_inside_card = (
        By.CSS_SELECTOR,
        "a[href]"
    )

    # Property Cards
    property_cards = (
        By.CSS_SELECTOR,
        "div[data-label='SEARCH'], "
        "section[data-cnstrc-item-name='propertyTuple'], "
        "div[data-cnstrc-item-name='propertyTuple']"
    )

    results_heading = (
        By.TAG_NAME,
        "h1"
    )

    result_count_text = (
        By.XPATH,
        "//*[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'results')]"
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

            visible_element = elements[0]

            self.driver.execute_script(
                "arguments[0].click();",
                visible_element
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

    def click_ok_understood(self):

        return self.handle_blocking_popups()

    def wait_for_filter_update(self):

        try:
            self.wait.until(
                EC.invisibility_of_element_located(
                    self.loading_placeholder
                )
            )

        except TimeoutException:
            pass

        self.wait.until(
            lambda driver: len(
                self.get_visible_property_cards()
            ) > 0
        )

    def get_visible_property_cards(self):

        cards = self.driver.find_elements(
            *self.property_cards
        )

        visible_cards = []

        for card in cards:
            try:
                if card.is_displayed():
                    visible_cards.append(card)

            except StaleElementReferenceException:
                continue

        return visible_cards

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
                    "window.scrollBy(0, Math.floor(window.innerHeight * 0.65));"
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

    def find_visible_element_from_locators(self, locators, timeout=10):

        last_error = None

        for locator in locators:
            try:
                return self.find_visible_element(
                    locator,
                    timeout=timeout
                )

            except TimeoutException as error:
                last_error = error

        raise last_error

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

    def click_filter(self, locator):

        self.handle_blocking_popups()

        # Wait for filter element
        filter_element = self.find_visible_element(
            locator
        )

        self.scroll_to_and_click(
            filter_element
        )

        # Wait for dynamic page refresh
        self.wait_for_filter_update()

        self.handle_blocking_popups()

    def open_locality_section(self):

        try:
            locality_section = self.find_visible_element(
                self.locality_section
            )

            self.scroll_to_and_click(
                locality_section
            )

        except TimeoutException:
            pass

    def apply_text_filter_if_visible(self, locator):

        filter_element = self.wait.until(
            EC.presence_of_element_located(
                locator
            )
        )

        self.scroll_to_and_click(
            filter_element
        )

        self.wait_for_filter_update()

    def switch_to_new_window(self, old_windows):

        try:
            self.wait.until(
                lambda driver: len(driver.window_handles) > len(old_windows)
            )

        except TimeoutException:
            return self.driver.current_window_handle

        new_window = [
            window
            for window in self.driver.window_handles
            if window not in old_windows
        ][0]

        self.driver.switch_to.window(
            new_window
        )

        return new_window

    # =========================
    # FILTER METHODS
    # =========================

    def apply_2_bhk_filter(self):

        self.click_filter(
            self.bhk_2_filter
        )

    def apply_independent_house_filter(self):

        self.handle_blocking_popups()

    def apply_residential_apartment_filter(self):

        self.click_filter(
            self.residential_apartment_filter
        )

    def apply_ready_to_move_filter(self):

        self.click_filter(
            self.ready_to_move_filter
        )

    def apply_rera_approved_filter(self):

        try:
            self.click_filter(
                self.rera_approved_filter
            )

            return True

        except TimeoutException:
            print(
                "RERA Approved filter was not available on the current results page"
            )

            return False

        try:
            house_filter = self.find_visible_element(
                self.independent_house_filter,
                max_scrolls=5,
                timeout=3
            )

        except TimeoutException:
            # Open Property Type Section
            property_section = self.wait.until(
                EC.presence_of_element_located(
                    self.property_type_section
                )
            )

            self.scroll_to_and_click(
                property_section
            )

            house_filter = self.find_visible_element(
                self.independent_house_filter,
                max_scrolls=5,
                timeout=10
            )

        self.scroll_to_and_click(
            house_filter
        )

        # Wait for dynamic refresh
        self.wait_for_filter_update()

        self.handle_blocking_popups()

    def apply_owner_filter(self):

        self.driver.execute_script(
            "window.scrollTo(0, 0);"
        )

        self.click_filter(
            self.owner_filter
        )

    def apply_locality_filter(self):

        self.handle_blocking_popups()

        self.open_locality_section()

        try:
            locality_option = self.find_visible_element_from_locators(
                (
                    self.hitech_city_filter,
                    self.locality_filter_options
                ),
                timeout=5
            )

        except TimeoutException:
            print(
                "Locality filter was not available on the current results page"
            )

            return False

        self.scroll_to_and_click(
            locality_option
        )

        self.wait_for_filter_update()

        self.handle_blocking_popups()

        return True

    # =========================
    # VALIDATION
    # =========================

    def get_results_count(self):

        count = self.get_results_count_from_visible_text()

        if count is not None:
            return count

        results = self.get_visible_property_cards()

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

        candidates = []

        headings = self.driver.find_elements(
            *self.results_heading
        )

        elements = self.driver.find_elements(
            *self.result_count_text
        )

        for element in headings + elements:
            try:
                if element.is_displayed():
                    candidates.append(
                        element.text
                    )

            except StaleElementReferenceException:
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

    def verify_filtered_results(self):

        results = self.wait.until(
            EC.visibility_of_any_elements_located(
                self.property_cards
            )
        )

        print(
            "Filtered Results Found:",
            self.get_results_count()
        )

        return len(results) > 0

    def get_first_result_card(self):

        return self.wait.until(
            lambda driver: self.get_visible_property_cards()[0]
            if self.get_visible_property_cards()
            else False
        )

    def get_first_result_click_target(self):

        first_result = self.get_first_result_card()

        links = first_result.find_elements(
            *self.property_link_inside_card
        )

        for link in links:
            try:
                href = link.get_attribute(
                    "href"
                )

                if (
                    href
                    and href.startswith("http")
                    and link.is_displayed()
                ):
                    return link

            except StaleElementReferenceException:
                continue

        return first_result

    def select_first_result(self):

        self.handle_blocking_popups()

        first_result_target = self.get_first_result_click_target()

        old_windows = self.driver.window_handles

        self.scroll_to_and_click(
            first_result_target
        )

        self.switch_to_new_window(
            old_windows
        )

        self.handle_blocking_popups()

        return True

    def verify_property_detail_page_opened(self):

        self.wait.until(
            lambda driver: driver.current_url
            and driver.current_url != "about:blank"
        )

        page_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        return (
            "99acres" in self.driver.current_url
            and (
                "Property" in page_text
                or "Bedroom" in page_text
                or "Contact" in page_text
                or "View Number" in page_text
            )
        )
