import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def userinfo_test(driver):
    print("UPDATER USER INFO TEST...")

    # scroll down
    driver.find_element_by_tag_name('main').send_keys(Keys.PAGE_DOWN)
    wait = WebDriverWait(driver, 3)

    # update email
    email = driver.find_element_by_id('email')
    email.clear(); time.sleep(0.5)
    email.send_keys("newemail"); time.sleep(0.5)
    email.send_keys("@test.com"); time.sleep(1)

    # update education level
    edulevel = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-id='inputEduLevel']")))
    edulevel.click(); time.sleep(1)
    edulevel.send_keys('Doc'); time.sleep(0.5)
    edulevel.send_keys(Keys.RETURN)
    time.sleep(1)

    # click submit
    submit = wait.until(EC.element_to_be_clickable((By.ID, 'update-info-button')))
    submit.click()

    return

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    userinfo_test(driver)
