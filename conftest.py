import pytest
from selenium import webdriver

# decorator 
@pytest.fixture
# setup and teardown
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    # yield is for thora ruk ja pehle dusra kam ho raha fir karenge 
    yield driver
    driver.quit()