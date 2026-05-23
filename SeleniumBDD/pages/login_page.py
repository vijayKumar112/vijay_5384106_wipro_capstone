from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait


class LoginPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 40)

        self.actions = ActionChains(driver)

    # =========================
    # LOCATORS
    # =========================

    # Profile Icon
    profile_icon = (
        By.XPATH,
        "//*[@id='app']/div/div[1]/div[2]/div[2]/div[5]"
    )

    # Login/Register Button
    login_register_button = (
        By.XPATH,
        "//div[contains(text(),'LOGIN / REGISTER')]"
    )

    # Mobile Number Input
    mobile_input = (
        By.CSS_SELECTOR,
        "#app > div > div.component__dialogueBox > div.component__body > div.loginRegisterStyle__mobwebLoginGui > div > div > form > div.inputWrap__inputWrap > div > div > input"
    )

    # Continue Button
    continue_button = (By.XPATH,"//button[normalize-space()='Continue']")

    verify_continue_button = (
        By.XPATH,
        "//button[contains(.,'Verify')]"
    )

   #pop ups
    overlay = (
        By.CSS_SELECTOR,
        ".component__overlayBg"
    )

    # =========================
    # ACTIONS
    # =========================

    def hover_profile_icon(self):

        profile = self.wait.until(
            EC.visibility_of_element_located(
                self.profile_icon
            )
        )

        self.actions.move_to_element(
            profile
        ).perform()

    def click_login_register(self):

        login_btn = self.wait.until(
            EC.element_to_be_clickable(
                self.login_register_button
            )
        )

        login_btn.click()

    def enter_mobile_number(self, mobile):
        mobile_field = self.wait.until(
            EC.element_to_be_clickable(
                self.mobile_input
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            mobile_field
        )

        mobile_field.click()

        mobile_field.clear()

        mobile_field.send_keys(str(mobile))



    def click_continue(self):
        continue_btn = self.wait.until(
            EC.element_to_be_clickable(
                self.continue_button
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            continue_btn
        )

        continue_btn.click()

    def click_verify_and_continue(self):
        verify_btn = self.wait.until(
            EC.element_to_be_clickable(
                self.verify_continue_button
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            verify_btn
        )

        verify_btn.click()

    #Closing pop up
    def wait_for_overlay_to_disappear(self):
        self.wait.until(
            EC.invisibility_of_element_located(
                self.overlay
            )
        )

