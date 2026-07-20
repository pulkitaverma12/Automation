import os
import sys
import time
import pytest

# Adjust path to find pages and utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pages')))
from login_page import LoginPage
from home_page import HomePage
from utilities.excel_helper import ExcelHelper

def test_home_page_flow(driver):
    # 1. Read valid credentials from Excel
    EXCEL_FILE = "login_data.xlsx"
    test_cases = ExcelHelper.read_test_data(EXCEL_FILE)
    
    # Find the test case expected to succeed (e.g. TC01)
    tc_valid = None
    for tc in test_cases:
        if tc["ExpectedResult"].lower() == "success":
            tc_valid = tc
            break
            
    if not tc_valid:
        pytest.fail("No valid login test case (ExpectedResult='Success') found in Excel file.")
        
    username = tc_valid["Username"]
    password = tc_valid["Password"]
    
    # 2. Perform successful login
    login_page = LoginPage(driver)
    login_page.load()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_signin()
    
    # Wait for redirect
    time.sleep(3)
    assert login_page.is_login_successful(), "Login was not successful using the credentials from Excel."
    
    # 3. Instantiate HomePage
    home_page = HomePage(driver)
    
    # 4. Verify user profile name is displayed correctly
    profile_name = home_page.get_profile_name()
    assert profile_name == "Mitesh Chandra123", f"Expected profile name 'Mitesh Chandra123', but got '{profile_name}'"
    
    # 5. Verify layout: Create Post button is visible
    assert home_page.is_create_post_button_visible(), "Create post button is not visible on the homepage."
    
    # 6. Verify Navigation redirect to Explore
    home_page.click_navigation_link("Explore")
    time.sleep(2)
    assert "/explore" in driver.current_url.lower(), f"Expected to navigate to /explore, but current URL is: {driver.current_url}"
    
    # 7. Navigate back to Home
    home_page.click_navigation_link("Home")
    time.sleep(2)
    assert driver.current_url.rstrip("/").lower() == "https://stage.emilo.in", f"Expected to navigate back to homepage, but current URL is: {driver.current_url}"
