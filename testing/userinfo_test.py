import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def userinfo_test(driver):
    print("UPDATER USER INFO TEST...")
    return

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    userinfo_test(driver)
