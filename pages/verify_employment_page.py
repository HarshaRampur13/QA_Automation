from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class VerifyEmploymentPage(BasePage):

    PAGE_HEADING = (By.XPATH,
        "//*[contains(normalize-space(text()),'Verify the Employment')"
        " or contains(normalize-space(text()),'Verify Employment')]")

    # Select Partner: readonly input inside floating-label-input with label 'Select Partner'
    PARTNER_INPUT = (By.XPATH,
        "//div[contains(@class,'floating-label-input')]"
        "[.//label[contains(text(),'Select Partner')]]//input")

    # Employee Name input
    EMPLOYEE_NAME_INPUT = (By.XPATH,
        "//div[contains(@class,'floating-label-input')]"
        "[.//label[contains(text(),'Employee Name')]]//input")

    # Employee Code input
    EMPLOYEE_CODE_INPUT = (By.XPATH,
        "//div[contains(@class,'floating-label-input')]"
        "[.//label[contains(text(),'Employee Code')]]//input")

    # PROCEED button
    PROCEED_BTN = (By.XPATH,
        "//button[normalize-space(text())='PROCEED' or normalize-space(text())='Proceed']")

    # Loader
    LOADER = (By.CSS_SELECTOR, ".loader-container, .loader")

    def is_page_loaded(self):
        return self.is_displayed(self.PAGE_HEADING, timeout=20)

    def _wait_loader_gone(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.LOADER))
        except Exception:
            pass

    def fill_and_proceed(self, employer: str, name: str, emp_id: str):
        # Step 1: Select Partner — click picker, search in drawer, click option
        try:
            partner_input = self.find_visible(self.PARTNER_INPUT)
            current_val = partner_input.get_attribute("value")
            print(f"\n[DEBUG] Current partner value: '{current_val}'")

            if not current_val:  # Only select if not already filled by HRMS
                self.driver.execute_script("arguments[0].click();", partner_input)
                time.sleep(1.5)

                # Type in the search box inside the drawer to filter options
                search_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@data-testid='drawer-wrapper']//input"
                                   " | //div[contains(@class,'rs-drawer')]//input")))
                search_input.send_keys(employer)
                time.sleep(1)
                print(f"\n[DEBUG] Typed '{employer}' in search box")

                # Click the matching option (use contains for partial match)
                option_xpath = f"//*[contains(normalize-space(text()),'{employer}')]"
                option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, option_xpath)))
                self.driver.execute_script("arguments[0].click();", option)
                time.sleep(0.5)
                print(f"\n[OK] Partner selected: {employer}")
            else:
                print(f"\n[INFO] Partner already filled by HRMS: {current_val}")
        except Exception as e:
            print(f"\n[WARN] Partner selection failed: {e}")
            # Close the drawer if still open so inputs are accessible
            try:
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                time.sleep(0.5)
                print("\n[INFO] Drawer closed via Escape")
            except Exception:
                pass

        # Wait for any smallModal to disappear after partner selection
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".smallModal, .rs-modal-xs")))
            print("\n[DEBUG] smallModal dismissed")
        except Exception:
            pass
        time.sleep(0.5)

        # Step 2: Employee Name — fill only if empty using JS to avoid interception
        try:
            name_input = self.find_visible(self.EMPLOYEE_NAME_INPUT)
            if not name_input.get_attribute("value"):
                self.driver.execute_script(
                    "var n=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                    "n.call(arguments[0],arguments[1]);"
                    "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                    "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                    name_input, name)
                print(f"\n[OK] Employee name entered: {name}")
            else:
                print(f"\n[INFO] Employee name already filled: {name_input.get_attribute('value')}")
        except Exception as e:
            print(f"\n[WARN] Employee name failed: {e}")

        # Step 3: Employee Code — fill only if empty using JS
        try:
            code_input = self.find_visible(self.EMPLOYEE_CODE_INPUT)
            if not code_input.get_attribute("value"):
                self.driver.execute_script(
                    "var n=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                    "n.call(arguments[0],arguments[1]);"
                    "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                    "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                    code_input, emp_id)
                print(f"\n[OK] Employee code entered: {emp_id}")
            else:
                print(f"\n[INFO] Employee code already filled: {code_input.get_attribute('value')}")
        except Exception as e:
            print(f"\n[WARN] Employee code failed: {e}")

        time.sleep(0.5)

        # Step 4: Click PROCEED and wait up to 120 seconds for URL to change
        self.click(self.PROCEED_BTN)
        print("\n[OK] PROCEED clicked — waiting up to 120 seconds for navigation...")
        try:
            WebDriverWait(self.driver, 120).until(
                lambda d: "employment-verification" not in d.current_url)
            print(f"\n[OK] Navigation complete — URL: {self.driver.current_url}")
        except Exception:
            print(f"\n[WARN] Navigation timeout — URL: {self.driver.current_url}")
