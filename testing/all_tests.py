import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from signup_test import signup_test
from search_test import search_test
from graph_test import graph_test
from logout_test import logout_test
from login_test import login_test
from userimage_test import userimage_test
from userdesc_test import userdesc_test
from userinfo_test import userinfo_test

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("http://localhost:8080/")

    signup_test(driver)
    search_test(driver)
    graph_test(driver)
    logout_test(driver)
    login_test(driver)
    userimage_test(driver)
    userdesc_test(driver)
    userinfo_test(driver)
