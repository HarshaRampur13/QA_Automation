from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class OtpPage(BasePage):

    # 6 individual digit boxes — each is input[type='number']
    OTP_INPUTS  = (By.CSS_SELECTOR, "input[type='number']")
    SUBMIT_BTN  = (By.XPATH, "//button[normalize-space(text())='SUBMIT']")

    def is_otp_page_loaded(self, timeout=30):
        """Wait for OTP modal to appear — increased timeout to handle server throttling."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.OTP_INPUTS))
            return True
        except Exception:
            return False

    def verify_otp(self, otp: str):
        """Wait for user to manually enter OTP in Chrome browser.
        As soon as all digits are entered and SUBMIT becomes enabled, auto-clicks it."""
        print("\n" + "="*50)
        print("[!!] OTP screen is open in Chrome!")
        print("[>>] Enter your OTP manually in the browser window")
        print("[..] SUBMIT will be clicked automatically once enabled")
        print("="*50)

        # Poll every second — click SUBMIT the moment it becomes enabled (max 120s)
        try:
            WebDriverWait(self.driver, 120).until(
                lambda d: "disabled" not in
                d.find_element(*self.SUBMIT_BTN).get_attribute("class"))
            # Re-find to avoid stale element
            self.driver.find_element(*self.SUBMIT_BTN).click()
            print("[OK] SUBMIT auto-clicked after OTP entry")
            time.sleep(3)
        except Exception as e:
            print(f"[WARN] SUBMIT click failed: {e}")
