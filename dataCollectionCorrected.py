from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import re,getpass,csv
import datetime
import random

def screenpos():
    driver.set_window_size(4031,1031)
    driver.set_window_position(-8,0)
    time.sleep(1)

PATH = "chromedriver"
# PATH = "/home/captain/Social Networks/Soical Project/Data Collection/chromedriver"

with open("data.txt") as f:
    lines = f.read().splitlines() 

data = open("DataCorrect.txt","a")
check = 0

for users in lines:
    check += 1
    if(check<1620): 
        continue
    print(check)
    repos = []
    users = users.split()
    data.write('\n')
    user = users[0]
    data.write(user)
    path = "https://github.com/"+user+"?tab=repositories"
    driver = webdriver.Chrome(PATH)
    driver.minimize_window()
    driver.implicitly_wait(1)
    driver.get(path)
    try:
        user_repos = WebDriverWait(driver,5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#user-repositories-list > ul > li > div.col-10.col-lg-9.d-inline-block > div.d-inline-block.mb-1 > h3 > a')),
        )

        for repo in user_repos: 
            data.write(" "+repo.text)
            repos.append(repo.text)

    except TimeoutException:
        pass

    print(repos)

    driver.quit()