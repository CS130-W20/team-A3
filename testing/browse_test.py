import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def browse_test(driver):
    print("BROWSE MODE TEST...")
    
    # open browse bar
    driver.get("http://localhost:8080/#")
    time.sleep(2)

    # open information science, database, data mining
    wait = WebDriverWait(driver, 3)
    wait.until(EC.element_to_be_clickable((By.ID, "5"))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "17"))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "6"))).click()
    time.sleep(2)

    # close browse bar
    driver.find_element_by_id('-1').click()

    return

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    browse_test(driver)
