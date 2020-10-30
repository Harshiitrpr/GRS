from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from collections import defaultdict
import time
import re,getpass,csv
import datetime
import random
from collections import defaultdict

PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(1)
driver.minimize_window()    

with open("userFollowingData.txt") as f:
    lines = f.read().splitlines() 
    for users in lines:
        print('################### new user ###################')
        circle = users.split()
        user = circle[0]
        print(user)
        if len(circle) < 2:
            print('following no one')
            print('###############################################\n\n')
            
            continue
        following_users = circle[1:]
        userRepoType = []
        for following_user in following_users:
            url = "https://github.com/"+following_user
            print(url)
            driver.get(url)
            try:
                user_repos = WebDriverWait(driver,50).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div:nth-child(2) > div > div:nth-child(1) > div > ol > li > div > div > div > a > span')),
                )
                for repo in user_repos:
                    print('\t' + repo.text)

            except TimeoutException:
                pass
        print('#########################################\n\n')
