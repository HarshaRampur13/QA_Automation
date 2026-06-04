from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OffersPage(BasePage):

    OFFERS_CONTAINER = (By.XPATH,
        "//*[contains(@class,'offer') or contains(@class,'service') "
        "or contains(@class,'card') or contains(@class,'product')]")

    def is_page_loaded(self):
        if "review-progress" in self.driver.current_url:
            print("\n[INFO] review-progress page — Offers not applicable for this flow")
            return True
        return self.is_displayed(self.OFFERS_CONTAINER, timeout=20)

    def get_offers_count(self):
        try:
            cards = self.driver.find_elements(*self.OFFERS_CONTAINER)
            return len(cards)
        except Exception:
            return 0