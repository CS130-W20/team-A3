import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def search_test(driver):
    print("SEARCH TEST...")

    # search for term
    elem = driver.find_element_by_name("key_word")
    elem.clear()
    elem.send_keys("machine learning")
    elem.send_keys(Keys.RETURN)

    # tolerate spelling error within edit distance two
    elem = driver.find_element_by_name("key_word")
    elem.clear()
    elem.send_keys("machin leanning")
    elem.send_keys(Keys.RETURN)  

    # scroll down then up, then click on first result
    wait = WebDriverWait(driver, 10)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#doc ul p big a')))
    time.sleep(2)
    body = driver.find_element_by_id('main_div').send_keys(Keys.END)
    time.sleep(1)
    body = driver.find_element_by_id('main_div').send_keys(Keys.HOME)
    time.sleep(1)
    elem.click()
    time.sleep(2)

    # switch focus to new tab, scroll down and up
    driver.switch_to_window(driver.window_handles[1])
    body = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.HOME)
    time.sleep(2)

    # close new tab, go back to home
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    driver.find_element_by_css_selector('a.nav-link').click()


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")
    search_test(driver)
