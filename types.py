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

PATH = "chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(1)
driver.minimize_window()    

with open("DataCorrect.txt") as f:
    lines = f.read().splitlines() 
    for users in lines:
        repos = users.split()
        user = repos[0]
        repos = repos[1:]
        for repo in repos:
            url = "https://github.com/"+user+"/"+repo
            # print(url)
            driver.get(url)
            link = driver.find_elements_by_css_selector('#js-repo-pjax-container > div.container-xl.clearfix.new-discussion-timeline.px-3.px-md-4.px-lg-5 > div > div.gutter-condensed.gutter-lg.flex-column.flex-md-row.d-flex > div.flex-shrink-0.col-12.col-md-3 > div > div')[-1]
            # print("link",link)
            languages = link.find_elements_by_css_selector("div > ul > li > a > span.text-gray-dark.text-bold.mr-1")
            percentage = link.find_elements_by_css_selector("div > ul > li > a > span:nth-child(3)")
            for i in range(len(percentage)):
                perc = percentage[i].text
                perc = perc[:len(perc)-1]
                perc = float(perc)
                if(perc>20):
                    print(languages[i].text)
                    # print(languages[i].text)