import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL      = os.getenv("BASE_URL", "https://dev-pwa.instape.com")
    BROWSER       = os.getenv("BROWSER", "chrome")
    HEADLESS      = os.getenv("HEADLESS", "false").lower() == "true"
    EXPLICIT_WAIT   = int(os.getenv("EXPLICIT_WAIT", 20))
    MOBILE_VIEW     = os.getenv("MOBILE_VIEW", "false").lower() == "true"
    MOBILE_DEVICE   = os.getenv("MOBILE_DEVICE", "iPhone 12 Pro")
    USER_PHONE    = os.getenv("USER_PHONE", "9999999999")
    TEST_OTP      = os.getenv("TEST_OTP", "123456")
    EMPLOYER_NAME = os.getenv("EMPLOYER_NAME", "Rajasthan Gov")
    EMPLOYEE_NAME = os.getenv("EMPLOYEE_NAME", "Test User")
    EMPLOYEE_ID   = os.getenv("EMPLOYEE_ID", "EMP001")
    PAN_NUMBER    = os.getenv("PAN_NUMBER", "ABCDE1234F")
    EMAIL         = os.getenv("EMAIL", "harsha.rampur@Instape.com")