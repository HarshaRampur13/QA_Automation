from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PersonalDetailsPage(BasePage):

    PAGE_HEADING = (By.XPATH,
        "//*[contains(translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'personal')]")

    PROCEED_BTN = (By.XPATH,
        "//button[contains(translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'proceed')"
        " or contains(translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'next')]")

    def is_page_loaded(self):
        # For Rajasthan Govt flow, review-progress is the valid end state
        if "review-progress" in self.driver.current_url:
            print("\n[INFO] review-progress page — Personal Details not applicable")
            return True
        return self.is_displayed(self.PAGE_HEADING, timeout=15)

    def fill_and_proceed(self):
        if "review-progress" in self.driver.current_url:
            print("\n[INFO] Skipping Personal Details — on review-progress page")
            return
        import os
        try:
            src = self.driver.page_source
            path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'personal_page.html')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(src)
            print(f"\n[DEBUG] Personal page source saved | URL: {self.driver.current_url}")
        except Exception:
            pass
        self.click(self.PROCEED_BTN)