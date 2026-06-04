import pytest
from pages.login_page import LoginPage
from pages.otp_page import OtpPage
from pages.hrms_popup_page import HrmsPopupPage
from pages.verify_employment_page import VerifyEmploymentPage
from pages.home_page import HomePage
from pages.personal_details_page import PersonalDetailsPage
from pages.offers_page import OffersPage
from config.config import Config


class TestNewUserFlow:

    def test_tc01_login_page_loads(self, driver):
        """Verify login page loads correctly"""
        login = LoginPage(driver)
        assert "instape" in driver.current_url.lower()
        print("\n[PASS] TC01 — Login page loaded")

    def test_tc02_login_button_disabled_without_checkbox(self, driver):
        """LOGIN SECURELY button must stay disabled until T&C is checked"""
        login = LoginPage(driver)
        login.enter_phone(Config.USER_PHONE)
        btn_class = driver.find_element(*LoginPage.LOGIN_BTN).get_attribute("class")
        assert "disabled" in btn_class
        print("\n[PASS] TC02 — Login button correctly disabled without T&C")

    def test_tc03_otp_screen_appears_after_login(self, driver):
        """OTP input must appear after login"""
        login    = LoginPage(driver)
        otp_page = OtpPage(driver)
        login.login(Config.USER_PHONE)
        assert otp_page.is_otp_page_loaded()
        print("\n[PASS] TC03 — OTP screen appeared")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tc04_complete_new_user_flow_to_offers(self, driver):
        """Full new user flow — Login to Offers"""
        login      = LoginPage(driver)
        otp_page   = OtpPage(driver)
        hrms_popup = HrmsPopupPage(driver)
        verify_emp = VerifyEmploymentPage(driver)
        home       = HomePage(driver)
        personal   = PersonalDetailsPage(driver)
        offers     = OffersPage(driver)

        print(f"\n[Step 1] Login with phone: {Config.USER_PHONE}")
        login.login(Config.USER_PHONE)

        print(f"[Step 2] Enter OTP: {Config.TEST_OTP}")
        assert otp_page.is_otp_page_loaded()
        otp_page.verify_otp(Config.TEST_OTP)

        print("[Step 3] Handle HRMS popup")
        hrms_popup.handle_popup()

        print("[Step 4] Verify Employment")
        assert verify_emp.is_page_loaded()
        verify_emp.fill_and_proceed(
            employer=Config.EMPLOYER_NAME,
            name=Config.EMPLOYEE_NAME,
            emp_id=Config.EMPLOYEE_ID
        )

        print("[Step 5] Home page — give consent")
        assert home.is_page_loaded()
        home.consent_and_proceed()

        print("[Step 6] Personal Details")
        assert personal.is_page_loaded()
        personal.fill_and_proceed()

        print("[Step 7] Offers screen")
        assert offers.is_page_loaded(), \
            f"Offers screen should load. URL: {driver.current_url}"
        print(f"\n[PASS] TC04 — Complete flow done! URL: {driver.current_url}")