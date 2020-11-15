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

file1 = open("/home/captain/GRS/languages.txt", 'r')
lines = file1.read().splitlines()

token = 0
for i in lines:
    x = i.split(' ')
    if(len(x) == 2):
        tokenise[x[0]] = int(x[1])
        token = int(x[1])
    elif(len(x) == 3):
        tokenise[x[0] + ' ' +x[1]] = int(x[2])
        token = int(x[2])
    else:
        tokenise[x[0] + ' ' + x[1] + ' ' + x[2]] = int(x[3])
        token = int(x[3])
# PATH = "chromedriver.exe"
PATH = "/home/captain/GRS/chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(1)
driver.minimize_window()
recommendationx = open("Recommended-repos.txt", 'a')

with open("/home/captain/GRS/userFollowingData.txt") as f:
    lines = f.read().splitlines() 

with open("/home/captain/GRS/userRepoTypeInfo.txt") as fg:
    user_repo_pasand = fg.read().splitlines() 

for counter in range(len(lines)):
    users = lines[counter]
    followings = users.split()
    user = followings[0]
    following = followings[1:]
    userRepoType = []
    user_pasand = user_repo_pasand[counter].split(' ')
    user_pasand = user_pasand[1:]
    user_pasand_num=[]
    user_pasand_type=[]
    for c in range(len(user_pasand)):
        user_pasand_num.append(int(user_pasand[c].split('-')[1]))
        user_pasand_type.append(int(user_pasand[c].split('-')[0]))
    if(len(following)==0):
        recommendationx.write(user+'\n')
    for candidate in following:
        recommendationx.write(user + ' ' + candidate)
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
        repos=[]
        for repo in candidate_repos:
            repos.append(repo.text)
        for repo in repos: 
            name_repo=repo
            url = "https://github.com/"+candidate+"/"+name_repo
            try:
                driver.get(url)
            except:
                continue
            print(name_repo)
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
                    if(languages[i].text in tokenise):
                        if(tokenise[languages[i].text] in user_pasand_type):
                            recommendationx.write(' ' + name_repo + '-' + str(user_pasand_num[user_pasand_type.index(tokenise[languages[i].text])]))
            time.sleep(0.5)
        recommendationx.write('\n')

