# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:37:43 2021

@author: bobo
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import shutil
import requests
import re
from bs4 import BeautifulSoup

def mkdir(path):
    #判斷目錄是否存在
    #存在：True
    #不存在：False
    folder = os.path.exists(path)

    #判斷結果
    if not folder:
        #如果不存在，則建立新目錄
        os.makedirs(path)
        print('-----建立成功-----')

    else:
        #如果目錄已存在，則不建立，提示目錄已存在
        print(path+'目錄已存在')

options = webdriver.ChromeOptions()
#options.add_argument("--disable-notifications")
options.add_argument('--headless') # 啟動無頭模式
options.add_argument('--disable-gpu') # windowsd必須加入此行
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://140.124.182.129/Login")

account = driver.find_elements_by_id('account')
account[-1].send_keys('zero')
password = driver.find_element_by_id("passwd")
password.send_keys('14222017')
sleep(2)
password.send_keys(Keys.CONTROL, "\ue007")
sleep(2)

driver.get('http://140.124.182.129/ShowVClass?vclassid=1')

soup = BeautifulSoup(driver.page_source, 'lxml')
#print(soup)

urls = soup.find_all('a', {'href': re.compile('./ContestRanking.*')})
ranking = []
for link in urls:
    ranking.append(str(link['href'])[1:])
print(ranking)

for rank in ranking:
    try:
        contest = "http://140.124.182.129"+rank
        driver.get(contest)
        
        contestsoup = BeautifulSoup(driver.page_source, 'lxml')
        #print(contestsoup)
        
        homeworkChap = contestsoup.find('a', {'title': 'The Contest was created By [zero]'}).get_text()
        makedir = './'+ str(homeworkChap)
        mkdir(makedir)
        contesturls = contestsoup.find('a', {'href': re.compile('./ContestSubmissions.*')})
        contestranking = str(contesturls['href'])[1:]
        print(contestranking)
        
        submissions = "http://140.124.182.129" + contestranking
        
        driver.get(submissions)
        
        submissionssoup = BeautifulSoup(driver.page_source, 'lxml')
        
        homeworklist = []
        submissionsurls = submissionssoup.find_all('tr', {'solutionid' : re.compile(".*")})
        
        for step, i in enumerate(submissionsurls):
            try:
                name = i.find('a').get_text()
                homework = i.find('a', {'title' : '[]'}).get_text()
                acstyle = i.find('a', {'class': 'acstyle'}).get_text()
                homeworklist.append([step,name, homework, acstyle, ""])
            except:
                pass
        
        button = driver.find_elements_by_xpath("//button[@class='btn btn-default btn-xs' and @id='btn_SolutionCode']")
    
        for step,(i,a, b,c,d) in enumerate(homeworklist):
            try:
                print(step)
                button[i].click()
                sleep(1)
                codes = driver.find_elements_by_id("code")
                homeworklist[step][4] = codes[i*2].text
                print(codes[i*2].text)
                sleep(1)
                closes = driver.find_elements_by_xpath("//div[@class='modal-footer']/button[@class='btn btn-primary' and @type='button' and@data-dismiss='modal']")
                closes[i*3+1].click()
                sleep(2)
            except:
                pass
            
        for step,name,homework,asc,code in homeworklist:
            tempdir = makedir+'/'+name
            mkdir(tempdir)
            txt = tempdir+'/'+homework+'.txt'
            with open(txt, 'w') as f:
                f.write(code)
    except:
        pass
    
    



