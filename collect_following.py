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

with open("DataCorrect.txt") as f:
    lines = f.read().splitlines() 

data = open("userFollowingData.txt","a")
check = 0

driver = webdriver.Chrome(PATH)
driver.minimize_window()
tmp = 0

for users in lines:
    tmp+=1
    if(tmp<621):
        continue
    repos = []
    users = users.split()
    data.write('\n')
    user = users[0]
    data.write(user)
    path = "https://github.com/"+user+"?tab=following"
    driver.implicitly_wait(1)
    driver.get(path)
    check += 1
    print(check)
    try:
        user_following = WebDriverWait(driver,17).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div:nth-child(2) > div > div > div.d-table-cell.col-9.v-align-top.pr-3 > a > span.link-gray.pl-1')),
        )
        for repo in user_following:
            if(repo.text != ''):
                data.write(" "+repo.text)
    except TimeoutException:
        pass
    driver.back()
    driver.back()

driver.quit()