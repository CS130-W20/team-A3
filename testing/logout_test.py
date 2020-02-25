import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def logout_test(driver):
    print("LOGOUT TEST...")

    # click logout button
    driver.find_element_by_css_selector("button[title^='Logout']").click()

    # click confimation in modal
    wait = WebDriverWait(driver, 3)
    time.sleep(2)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='logout();']")))
    elem.click()

    return

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    logout_test(driver)
