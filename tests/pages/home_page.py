from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://stage.emilo.in/"

        # Locators
        self.profile_name_locator = (By.XPATH, "//*[contains(text(), 'Mitesh Chandra123')]")
        self.create_post_btn = (By.XPATH, "//button[contains(text(), 'Create post')]")
        self.logout_btn = (By.XPATH, "//span[text()='Logout']")
        
    def get_profile_name(self, timeout=10):
        """Wait for profile elements to be present and return the text of the visible one."""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.profile_name_locator)
        )
        els = self.driver.find_elements(*self.profile_name_locator)
        for el in els:
            if el.is_displayed():
                text = el.text.strip()
                if text:
                    return text
        raise Exception("No visible profile name element found.")

    def is_create_post_button_visible(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.create_post_btn)
            )
            return True
        except:
            return False

    def click_navigation_link(self, name, timeout=5):
        """Clicks a navigation link by its aria-label (e.g. 'Explore', 'Home'), selecting the visible one."""
        locator = (By.XPATH, f"//a[@aria-label='{name}']")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        els = self.driver.find_elements(*locator)
        for el in els:
            if el.is_displayed():
                el.click()
                return
        raise Exception(f"No visible navigation link found for aria-label: {name}")

    def click_profile_dropdown(self, timeout=5):
        """Clicks the visible profile button displaying the user name to toggle the dropdown."""
        btn_locator = (By.XPATH, "//button[.//span[contains(text(), 'Mitesh Chandra123')]]")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(btn_locator)
        )
        els = self.driver.find_elements(*btn_locator)
        for el in els:
            if el.is_displayed():
                el.click()
                return
        # Fallback to click the span directly if button is not clickable
        span_locator = (By.XPATH, "//span[text()='Mitesh Chandra123']")
        els = self.driver.find_elements(*span_locator)
        for el in els:
            if el.is_displayed():
                el.click()
                return
        raise Exception("No visible profile button found to trigger logout dropdown.")

    def click_logout(self, timeout=5):
        """Opens profile dropdown and clicks Logout."""
        self.click_profile_dropdown(timeout)
        logout_el = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.logout_btn)
        )
        logout_el.click()
