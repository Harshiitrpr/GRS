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
        token = int(x[1])
    elif(len(x) == 3):
        tokenise[x[0] + ' ' +x[1]] = int(x[2])
        token = int(x[2])
    else:
        tokenise[x[0] + ' ' + x[1] + ' ' + x[2]] = int(x[3])
        token = int(x[3])
token += 1
to_write = []
writer = csv.writer(open('lang.csv', 'a'))
# PATH = "chromedriver.exe"
PATH = "/home/captain/Social Project/GRS/chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(1)
driver.minimize_window()    
data = open("languages.txt","a")
fileforuser = open("userRepoTypeInfo.txt", "a")


check = 0
with open("/home/captain/Social Project/GRS/DataCorrect.txt") as f:
    lines = f.read().splitlines() 
    for users in lines:
        driver = webdriver.Chrome(PATH)
        driver.implicitly_wait(1)
        repos = users.split()
        user = repos[0]
        repos = repos[1:]
        userRepoType = []
        if(user == 'vidavakil'):
            check = 1
        if(check == 0):
            continue
        for repo in repos:
            to_write.append([user, repo])
            url = "https://github.com/"+user+"/"+repo
            # print(url)
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
                    if languages[i].text not in tokenise:
                        data.write(languages[i].text + ' ' + str(token) + '\n')
                        tokenise[languages[i].text] = token
                        token += 1
                    to_write[-1].append(tokenise[languages[i].text])
                    userRepoType.append(tokenise[languages[i].text])
            writer.writerow(to_write[-1])
        fileforuser.write(user)
        if(len(userRepoType) > 0):
            d = defaultdict(int)
            for x in range(len(userRepoType)):
                d[userRepoType[x]] += 1
            for key, value in d.items():
                fileforuser.write(' ' + str(key) + '-' + str(value))
        fileforuser.write('\n')
        time.sleep(0.5)
    
