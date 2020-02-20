import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def login_test(driver):
    # click on login/register button
    elem = driver.find_elements_by_css_selector("#navbars_dropdowns button")[2]
    elem.click()

    # fill sign up box
    wait = WebDriverWait(driver, 10)
    user = wait.until(EC.element_to_be_clickable((By.ID, 'username')))
    pwrd = driver.find_element_by_id("password")
    cbox = driver.find_element_by_id("show_password_checkbox")

    user.clear()
    pwrd.clear()
    user.send_keys("demo_user")
    pwrd.send_keys("password"); time.sleep(1)
    cbox.click(); time.sleep(1); cbox.click()

    elem = driver.find_element_by_css_selector("button.btn.btn-secondary.pull-right")
    elem.click()

    # go to user home
    wait.until(EC.element_to_be_clickable((By.ID, 'home_entry'))).click()

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    login_test(driver)
