import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def graph_test(driver):
    driver.find_element_by_css_selector('a.nav-link.pointer').click()
    time.sleep(5)
    driver.find_element_by_css_selector('a.nav-link').click()
    return

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    graph_test(driver)
