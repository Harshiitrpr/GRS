from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import re,getpass,csv
import datetime
import random

def screenpos():
    driver.maximize_window()
    driver.set_window_size(4031,1031)
    driver.set_window_position(-8,0)
    time.sleep(1)

PATH = "/home/captain/Social Networks/Soical Project/Data Collection/chromedriver"
driver = webdriver.Chrome(PATH)
driver.minimize_window()
driver.implicitly_wait(1)
while(1):
    print("Enter the URL :-", end = ' ')
    url = input()
    driver.get(url)
    link = driver.find_elements_by_css_selector('a[class="link-gray-dark no-underline "]')[2]
    contributor = WebDriverWait(driver,6,0.5).until(
        EC.presence_of_element_located((By.LINK_TEXT, link.text)),
    )
    contributor.click()
    driver.maximize_window()
    screenpos()