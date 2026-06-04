from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from config.config import Config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def open(self, path=""):
        self.driver.get(f"{Config.BASE_URL.rstrip('/')}/{path.lstrip('/')}")

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.find_clickable(locator).click()

    def js_click(self, locator):
        self.driver.execute_script("arguments[0].click();", self.find(locator))

    def type_text(self, locator, text, clear=True):
        el = self.find_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def select_by_text(self, locator, text):
        Select(self.find(locator)).select_by_visible_text(text)

    def get_text(self, locator):
        return self.find_visible(locator).text.strip()

    def is_displayed(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, text, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text))

    def get_current_url(self):
        return self.driver.current_url

    def take_screenshot(self, name):
        import os
        os.makedirs("reports/screenshots", exist_ok=True)
        self.driver.save_screenshot(f"reports/screenshots/{name}.png")