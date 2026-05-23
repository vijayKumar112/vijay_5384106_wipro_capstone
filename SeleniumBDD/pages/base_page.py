from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config_reader import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.explicit_wait)

    def open_url(self, url):
        self.driver.get(url)
        self.close_popups()

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def visible_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def close_popups(self):
        popup_selectors = [
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.CSS_SELECTOR, ".close, .modal__close, .iconS_Common_24.icon_close"),
            (By.XPATH, "//button[contains(., 'Later') or contains(., 'Not now')]"),
        ]
        for locator in popup_selectors:
            try:
                WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(locator)).click()
            except TimeoutException:
                continue

    def page_contains(self, text):
        return text.lower() in self.driver.page_source.lower()

