from pages.base_page import BasePage
import time


class HrmsPopupPage(BasePage):

    def handle_popup(self):
        """HRMS popup auto-dismisses after 4-5 seconds — just wait it out."""
        print("\n[INFO] Waiting 5 seconds for HRMS popup to auto-dismiss...")
        time.sleep(5)
        print("\n[OK] HRMS popup wait done")
