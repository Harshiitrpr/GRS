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


tokenise = dict()
token = 1
to_write = [["Users"]]

PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(1)
driver.minimize_window()    
data = open("languages.txt","a")


with open("DataCorrect.txt") as f:
    lines = f.read().splitlines() 
    for users in lines:
        repos = users.split()
        user = repos[0]
        repos = repos[1:]
        to_write.append([user] + [0 for i in range(token-1)])
        for repo in repos:
            url = "https://github.com/"+user+"/"+repo
            # print(url)
            driver.get(url)
            try:
                link = WebDriverWait(driver,20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#js-repo-pjax-container > div.container-xl.clearfix.new-discussion-timeline.px-3.px-md-4.px-lg-5 > div > div.gutter-condensed.gutter-lg.flex-column.flex-md-row.d-flex > div.flex-shrink-0.col-12.col-md-3 > div > div')),
                )
            except TimeoutException:
                pass

            if(len(link)==0):
                continue
            else:
                link = link[-1]
            # print("link",link)
            languages = link.find_elements_by_css_selector("div > ul > li > a > span.text-gray-dark.text-bold.mr-1")
            percentage = link.find_elements_by_css_selector("div > ul > li > a > span:nth-child(3)")
            for i in range(len(percentage)):
                perc = percentage[i].text
                perc = perc[:len(perc)-1]
                perc = float(perc)
                if(perc>20):
                    if languages[i].text not in tokenise:
                        data.write(languages[i].text + ' ')
                        tokenise[languages[i].text] = token
                        token += 1
                        to_write[0].append(languages[i].text)
                        for j in range(1,len(to_write)):
                            to_write[j].append(0)
                    to_write[-1][tokenise[languages[i].text]] += 1
        writer = csv.writer(open('lang.csv', 'w'))
        writer.writerows(to_write)
        time.sleep(0.5)