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

tokenise = dict()

file1 = open("/home/captain/Social Project/languages.txt", 'r')
lines = file1.read().splitlines()

token = 0
for i in lines:
    x = i.split(' ')
    if(len(x) == 2):
        tokenise[x[0]] = int(x[1])
    else:
        tokenise[x[0] + ' ' +x[1]] = int(x[2])
# PATH = "chromedriver.exe"
PATH = "/home/captain/Social Project/GRS/chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(1)
driver.minimize_window()
recommendation = open("Recommended-repos.txt", 'a')

with open("/home/captain/Social Project/GRS/userFollowingData.txt") as f:
    lines = f.read().splitlines() 

with open("/home/captain/Social Project/GRS/userRepoTypeInfo.txt") as fg:
    user_repo_pasand = fg.read().splitlines() 

for counter in range(len(lines)):
    users = lines[counter]
    followings = users.split()
    user = followings[0]
    following = followings[1:]
    userRepoType = []
    user_pasand = user_repo_pasand[counter].split(' ')
    user_pasand = user_pasand[1:]
    for c in range(len(user_pasand)):
        user_pasand[c] = int(user_pasand[c].split('-')[0])
    for candidate in following:
        recommendation.write(user + ' ' + candidate)
        path = "https://github.com/"+candidate+"?tab=repositories"
        driver.minimize_window()
        driver.implicitly_wait(1)
        driver.get(path)
        try:
            candidate_repos = WebDriverWait(driver,5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#user-repositories-list > ul > li > div.col-10.col-lg-9.d-inline-block > div.d-inline-block.mb-1 > h3 > a')),
            )

        except TimeoutException:
            pass
        for repo in candidate_repos: 
            url = "https://github.com/"+user+"/"+repo
            driver.get(url)
            try:
                link = WebDriverWait(driver,100).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#js-repo-pjax-container > div.container-xl.clearfix.new-discussion-timeline.px-3.px-md-4.px-lg-5 > div > div.gutter-condensed.gutter-lg.flex-column.flex-md-row.d-flex > div.flex-shrink-0.col-12.col-md-3 > div > div')),
                )
            except TimeoutException:
                continue

            if(len(link)==0):
                continue
            else:
                link = link[-1]
            # print("link",link)
            try:
                languages = link.find_elements_by_css_selector("div > ul > li > a > span.text-gray-dark.text-bold.mr-1")
                percentage = link.find_elements_by_css_selector("div > ul > li > a > span:nth-child(3)")
            except:
                continue
            for i in range(len(percentage)):
                perc = percentage[i].text
                perc = perc[:len(perc)-1]
                perc = float(perc)
                if(perc>=15):
                    if(tokenise[languages[i].text] in user_pasand):
                        recommendation.write(' ' + repo)
        recommendation.write('\n')

