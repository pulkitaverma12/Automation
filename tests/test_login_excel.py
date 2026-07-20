import os
import sys
import time
import pytest
from selenium.webdriver.common.by import By

# Adjust path to find pages and utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pages')))
from login_page import LoginPage
from utilities.excel_helper import ExcelHelper

EXCEL_FILE = "login_data.xlsx"

# Make sure template exists and read test data
ExcelHelper.create_default_template(EXCEL_FILE)
test_cases = ExcelHelper.read_test_data(EXCEL_FILE)

# Ensure screenshots directory exists
os.makedirs("screenshots", exist_ok=True)

@pytest.mark.parametrize("tc", test_cases, ids=lambda x: x["TestCaseID"])
def test_login_flow(driver, tc):
    tc_id = tc["TestCaseID"]
    username = tc["Username"]
    password = tc["Password"]
    expected_result = tc["ExpectedResult"]
    
    login_page = LoginPage(driver)
    
    # 1. Load the login page
    login_page.load()
    
    # 2. Enter credentials and click Sign in
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_signin()
    
    # Wait for the system to process the login
    time.sleep(3)
    
    actual_status = "Fail"
    actual_message = ""
    
    # 3. Verify based on expected outcome
    if expected_result.lower() == "success":
        # We expect a successful login (redirect away from /login)
        if login_page.is_login_successful():
            actual_status = "Pass"
            actual_message = f"Successfully logged in. Redirected to: {driver.current_url}"
        else:
            # Check if there is an error toast message
            err_msg = login_page.get_error_message()
            actual_message = f"Login failed as expected, but expected Success. Error Toast: {err_msg}"
    else:
        # We expect a failed login (error message/toast)
        err_msg = login_page.get_error_message()
        if err_msg:
            actual_status = "Pass"
            actual_message = f"Failed as expected with error: {err_msg}"
        elif login_page.is_login_successful():
            actual_message = "Unexpected successful login (expected failure)."
        else:
            actual_message = "Failed to login, but did not detect the expected error toast message."
            
    # 4. Take a screenshot
    screenshot_name = f"{tc_id}_{actual_status}_{int(time.time())}.png"
    screenshot_path = os.path.abspath(os.path.join("screenshots", screenshot_name))
    driver.save_screenshot(screenshot_path)
    
    # 5. Write status and embed screenshot into Excel
    try:
        ExcelHelper.update_test_result(
            file_path=EXCEL_FILE,
            tc_id=tc_id,
            status=actual_status,
            actual_message=actual_message,
            screenshot_path=screenshot_path
        )
    except Exception as e:
        print(f"Failed to update Excel file: {e}")
        
    # 6. Assert for pytest report
    assert actual_status == "Pass", f"Test {tc_id} failed: {actual_message}"
