from selenium import webdriver
from config.config import Config


def get_driver():
    options = webdriver.ChromeOptions()
    if Config.HEADLESS:
        options.add_argument("--headless")
    if Config.MOBILE_VIEW:
        options.add_experimental_option("mobileEmulation", {"deviceName": Config.MOBILE_DEVICE})
    else:
        options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver