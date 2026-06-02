import pytest
import os
from utils.driver_setup import get_driver
from config.config import Config


@pytest.fixture(scope="function")
def driver():
    _driver = get_driver()
    _driver.get(Config.BASE_URL + "/login")
    yield _driver
    _driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        d = item.funcargs.get("driver")
        if d:
            try:
                screenshots_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
                os.makedirs(screenshots_dir, exist_ok=True)
                path = os.path.join(screenshots_dir, f"{item.name}_FAILED.png")
                d.save_screenshot(path)
                print(f"\n[Screenshot saved] {path}")
            except Exception as e:
                print(f"\n[Screenshot skipped] Driver session unavailable: {e}")