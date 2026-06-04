from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time


class LoginPage(BasePage):

    # Phone input: <input maxlength="10" type="tel">
    PHONE_INPUT   = (By.CSS_SELECTOR, "div.floating-label-input input[type='tel']")

    # Checkbox: readonly input (React-controlled state), checkmark span is the clickable trigger
    TC_CHECKBOX   = (By.CSS_SELECTOR, "div.checkboxContainer input[type='checkbox']")
    CHECKMARK     = (By.CSS_SELECTOR, "span.checkmark")

    # Login button
    LOGIN_BTN     = (By.CSS_SELECTOR, "button.submitButton")

    # T&C / Privacy Policy modal
    TNC_MODAL     = (By.CSS_SELECTOR, ".tncModalDialog")
    VIEW_MORE_BTN = (By.XPATH, "//div[contains(@class,'tncModalDialog')]//button[normalize-space(text())='View More']")
    I_AGREE_BTN   = (By.XPATH, "//div[contains(@class,'tncModalDialog')]//button[normalize-space(text())='I AGREE']")

    LOADER        = (By.CSS_SELECTOR, ".loader-container")

    def open_login_page(self):
        self.open("/login")

    def enter_phone(self, phone: str):
        print(f"\n[DEBUG] Attempting to enter phone: '{phone}'")
        el = self.find_visible(self.PHONE_INPUT)
        el.click()
        time.sleep(0.3)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)
        el.send_keys(phone)
        time.sleep(0.3)
        print(f"\n[DEBUG] Phone entered: '{el.get_property('value')}'")

    def _wait_for_loader(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOADER))
        except Exception:
            pass

    def _action_click(self, locator):
        el = self.find_visible(locator)
        ActionChains(self.driver).move_to_element(el).click().perform()

    def _handle_modal_agree(self):
        """Handle T&C and Privacy Policy modals — click View More until I AGREE appears, then agree."""
        for round_num in range(5):
            if not self.is_displayed(self.TNC_MODAL, timeout=3):
                break
            try:
                heading = self.driver.find_element(By.CSS_SELECTOR, '.tncModalDialog h3').text
                print(f"\n[DEBUG] Modal round {round_num + 1}: '{heading}'")
            except Exception:
                print(f"\n[DEBUG] Modal round {round_num + 1}: heading not found")
            # Click View More until it disappears
            while self.is_displayed(self.VIEW_MORE_BTN, timeout=3):
                self._action_click(self.VIEW_MORE_BTN)
                time.sleep(0.3)
            # Click I AGREE
            if self.is_displayed(self.I_AGREE_BTN, timeout=5):
                self._action_click(self.I_AGREE_BTN)
                time.sleep(0.5)

    def accept_terms_and_conditions(self):
        """Click the checkmark span to open T&C modal, then agree to all modals."""
        # The checkmark span (not the text link) is the correct trigger for the T&C modal
        self._action_click(self.CHECKMARK)
        self.find_visible(self.TNC_MODAL)
        self._handle_modal_agree()
        print("\n[OK] T&C / Privacy Policy accepted")

    def _is_checkbox_checked(self):
        """Check if the readonly checkbox input is selected (React sets this after agreeing)."""
        try:
            checkbox = self.driver.find_element(*self.TC_CHECKBOX)
            return checkbox.is_selected()
        except Exception:
            return False

    def click_login_securely(self):
        self._wait_for_loader()
        btn_class = self.find(self.LOGIN_BTN).get_attribute("class")
        print(f"\n[DEBUG] Button class: {btn_class}")
        self.wait.until(lambda d:
            "disabled" not in d.find_element(*self.LOGIN_BTN).get_attribute("class"))
        self._action_click(self.LOGIN_BTN)
        print("\n[OK] LOGIN SECURELY clicked")

    def login(self, phone: str):
        self.enter_phone(phone)
        self.accept_terms_and_conditions()
        print(f"\n[DEBUG] Checkbox checked after T&C: {self._is_checkbox_checked()}")
        self.click_login_securely()
