import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from os import getcwd

def userimage_test(driver):
    print("UPDATE USER IMAGE TEST...")

    # click avatar
    driver.find_element_by_id('avatar-icon').click()
    time.sleep(2)

    # upload file
    wait = WebDriverWait(driver, 3)
    fileupload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='photo']")))
    maindir = '/'.join(getcwd().split('/')[:-1])
    fileupload.send_keys(maindir + "/static/img/users/7.gif")
    time.sleep(1)

    # confirm
    driver.find_element_by_css_selector("input[value='Upload']").click()

    return

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    userimage_test(driver)
