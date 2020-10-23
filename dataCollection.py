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
    driver.maximize_window()
    driver.set_window_size(4031,1031)
    driver.set_window_position(-8,0)
    time.sleep(1)

# PATH = "chromedriver"
PATH = "/home/captain/Social Networks/Soical Project/Data Collection/chromedriver"

with open("/home/captain/Social Networks/Soical Project/Data Collection/urls.txt") as f:
    lines = f.read().splitlines() 

check = 0
for url in lines:
    check += 1
    if(check < 7):
        continue
    if(check >= 15):
        break
    driver = webdriver.Chrome(PATH)
    screenpos()
    driver.implicitly_wait(1)
    check += 1
    driver.get(url)
    link = driver.find_element_by_css_selector('#js-repo-pjax-container > div.container-xl.clearfix.new-discussion-timeline.px-3.px-md-4.px-lg-5 > div > div.gutter-condensed.gutter-lg.flex-column.flex-md-row.d-flex > div.flex-shrink-0.col-12.col-md-3 > div')
    link = link.find_element_by_partial_link_text('Contributors') #div.BorderGrid-cell > h2.h4 > a[class="link-gray-dark no-underline "]
    # print(link.text)
    try:
        repo_contributors = WebDriverWait(driver,6,0.5).until(
            EC.presence_of_element_located((By.LINK_TEXT, link.text)),
        )
        repo_contributors.click()
    except TimeoutException:
        pass
    num_contributors = WebDriverWait(driver,100).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="contributors"]/ol/li/span/h3/a[2]')),
    )
    
    length = len(num_contributors)
    # if(length > 1000):
    #     length = 1000
    contributors = []
    repos = []
    data = open("data.txt", 'a')
    for x in range(length): #len(contributor_repos)
        data.write('\n')
        path = '//*[@id="contributors"]/ol/li['+str(x+1)+']/span/h3/a[2]'
        try:
            contributor = WebDriverWait(driver,100).until(
                EC.presence_of_element_located((By.XPATH, path)),
            )
            contributors.append(contributor.text)
            data.write(contributor.text)
            contributor.click()
        except TimeoutException:
            pass
        user_repos = []
        try:
            user_repos = WebDriverWait(driver,50).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div:nth-child(2) > div > div:nth-child(1) > div > ol > li > div > div > div > a > span')),
            )
            for repo in user_repos:
                repos.append(repo.text)
                data.write(" "+repo.text)

        except TimeoutException:
            pass
        
        driver.back()
    check += 1
    driver.quit()
