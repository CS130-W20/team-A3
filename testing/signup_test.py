import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def signup_test(driver):
    print("SIGNUP TEST...")

    # click on login/register button
    elem = driver.find_elements_by_css_selector("#navbars_dropdowns button")[2]
    elem.click()

    # fill sign up box
    wait = WebDriverWait(driver, 10)
    user = wait.until(EC.element_to_be_clickable((By.ID, 'username')))
    pwrd = driver.find_element_by_id("password")
    cbox = driver.find_element_by_name("reg")
    sbox = driver.find_element_by_id("show_password_checkbox")

    user.clear()
    pwrd.clear()
    user.send_keys("demo_user")
    pwrd.send_keys("password")
    cbox.click()

    # fill in confirm password
    pwrd = wait.until(EC.element_to_be_clickable((By.ID, 'password_confirm')))
    pwrd.send_keys("password")
    sbox.click(); time.sleep(1); sbox.click()


    time.sleep(1)

    elem = driver.find_element_by_css_selector("button.btn.btn-secondary.pull-right")
    elem.click()

    # fill in full details page
    email = wait.until(EC.element_to_be_clickable((By.ID, 'inputEmail')))
    body  = driver.find_element_by_tag_name("body")
    fname = driver.find_element_by_id("inputFirstname")
    lname = driver.find_element_by_id("inputLastname")
    edlvl = driver.find_element_by_id("inputEduLevel")
    intrs = driver.find_element_by_css_selector("button.btn.dropdown-toggle")
    knowl = driver.find_element_by_css_selector("button[data-id='inputConcepts']")

    driver.execute_script("window.scrollBy(0,300)")
    time.sleep(1)

    email.send_keys('demo_user@gmail.com')
    fname.clear(); fname.send_keys('Demo')
    lname.clear(); lname.send_keys('User')
    time.sleep(1)

    edlvl.click(); time.sleep(1)
    edlvl.send_keys("m")
    edlvl.send_keys(Keys.RETURN)
    time.sleep(1)

    intrs.click(); time.sleep(1)
    intrs.send_keys("data"); time.sleep(0.5); intrs.send_keys(Keys.RETURN)

    intrs.click(); time.sleep(1)
    intrs.send_keys("algo"); time.sleep(0.5); intrs.send_keys(Keys.RETURN)
    time.sleep(0.5)

    knowl.click(); time.sleep(1)
    knowl.send_keys("ai"); time.sleep(0.5); knowl.send_keys(Keys.RETURN)
    time.sleep(1)

    # submit
    driver.find_element_by_css_selector("button.btn.btn-lg.btn-primary").click()
    time.sleep(2)

    # go to user home
    wait.until(EC.element_to_be_clickable((By.ID, 'home_entry'))).click()
    time.sleep(2)

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    signup_test(driver)
