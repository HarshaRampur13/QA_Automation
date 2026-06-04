from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class HomePage(BasePage):

    LOADER       = (By.CSS_SELECTOR, ".loader-container, .loader")

    # Home screen identifier — "Get Your Salary Anytime" banner or CHECK LIMIT button
    PAGE_HEADING = (By.XPATH,
        "//*[contains(normalize-space(text()),'Get Your Salary Anytime')"
        " or normalize-space(text())='CHECK LIMIT']")

    # Consent circle (custom checkmark, same pattern as login page)
    CONSENT_CIRCLE = (By.CSS_SELECTOR, "span.checkmark, input[type='checkbox']")

    # CHECK LIMIT button
    CHECK_LIMIT_BTN = (By.XPATH,
        "//button[normalize-space(text())='CHECK LIMIT']")

    def _wait_for_loader(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.LOADER))
        except Exception:
            pass

    def is_page_loaded(self):
        self._wait_for_loader(timeout=30)
        url = self.driver.current_url
        # Accept home-screen OR review-progress as valid next pages
        if "review-progress" in url:
            print(f"\n[INFO] Review in Progress page — URL: {url}")
            return True
        result = self.is_displayed(self.PAGE_HEADING, timeout=20)
        print(f"\n[DEBUG] Home page loaded: {result} | URL: {url}")
        return result

    def consent_and_proceed(self):
        if "review-progress" in self.driver.current_url:
            print("\n[INFO] On review-progress page — skipping consent")
            return
        # Dump page source for debugging
        import os
        try:
            src = self.driver.page_source
            path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'home_page.html')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(src)
            print("\n[DEBUG] Home page source saved to reports/home_page.html")
        except Exception as e:
            print(f"\n[DEBUG] Page dump failed: {e}")

        # Click the consent circle using JS — try multiple selectors
        clicked = self.driver.execute_script("""
            var selectors = ['span.checkmark', 'input[type="checkbox"]',
                             '[role="button"]', '.checkboxContainer span',
                             '.tncBox span', '.consent span'];
            for (var s of selectors) {
                var el = document.querySelector(s);
                if (el) { el.click(); return 'clicked: ' + s; }
            }
            return 'not found';
        """)
        print(f"\n[DEBUG] Consent click: {clicked}")
        time.sleep(0.5)

        # Wait for CHECK LIMIT to become enabled and click it
        WebDriverWait(self.driver, 10).until(
            lambda d: "disabled" not in
            d.find_element(*self.CHECK_LIMIT_BTN).get_attribute("class"))
        self.find_visible(self.CHECK_LIMIT_BTN).click()
        print("\n[OK] CHECK LIMIT clicked")
