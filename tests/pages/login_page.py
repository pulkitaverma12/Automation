from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://stage.emilo.in/login"
        
        # Locators
        self.username_input = (By.NAME, "loginInput")
        self.password_input = (By.NAME, "password")
        self.signin_btn = (By.XPATH, "//button[@type='submit' and contains(text(), 'Sign in')]")
        self.error_toast = (By.CLASS_NAME, "Toastify__toast--error")

    def load(self):
        self.driver.get(self.url)
        # Wait until page loads by waiting for the username input to be visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        )

    def enter_username(self, username):
        el = self.driver.find_element(*self.username_input)
        el.clear()
        el.send_keys(username)

    def enter_password(self, password):
        el = self.driver.find_element(*self.password_input)
        el.clear()
        el.send_keys(password)

    def click_signin(self):
        self.driver.find_element(*self.signin_btn).click()

    def get_error_message(self, timeout=5):
        """Waits for and returns the error toast message text if it appears, otherwise None."""
        try:
            toast_el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error_toast)
            )
            return toast_el.text.strip()
        except:
            return None

    def is_login_successful(self, timeout=5):
        """Returns True if user is redirected or login succeeds (e.g. URL changes and does not contain /login)."""
        try:
            # Wait for URL to change from the login URL
            WebDriverWait(self.driver, timeout).until(
                lambda d: "/login" not in d.current_url
            )
            return True
        except:
            return False
