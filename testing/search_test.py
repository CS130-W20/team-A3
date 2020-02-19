import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://localhost:8080/")

# search for 'machine learning'
elem = driver.find_element_by_name("key_word")
elem.clear()
elem.send_keys("machine learning")
elem.send_keys(Keys.RETURN)

# scroll down then up, then click on first result
wait = WebDriverWait(driver, 10)
elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#doc ul p big a')))
body = driver.find_element_by_id('main_div').send_keys(Keys.END)
time.sleep(2)
body = driver.find_element_by_id('main_div').send_keys(Keys.HOME)
time.sleep(2)
elem.click()
