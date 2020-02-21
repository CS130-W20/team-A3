import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def userdesc_test(driver):
    print("UPDATE USER DESCRIPTION TEST...")

    # update text area
    textarea = driver.find_element_by_css_selector("textarea[aria-label='textarea']")
    textarea.clear()
    textarea.send_keys("Thanks "); time.sleep(0.5)
    textarea.send_keys("for "); time.sleep(0.5)
    textarea.send_keys("watching!");

    # click update button
    time.sleep(1)
    driver.find_element_by_id("update-description").click()

    return

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    userdesc_test(driver)
