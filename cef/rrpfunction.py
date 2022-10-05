
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from tqdm import tqdm

dfCef = pd.read_excel('cefScraping.xlsx')
path = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(path)

def rrpFunction(prodUrl):
    driver.set_page_load_timeout(30) 
    driver.get(prodUrl)
    rrp = driver.find_element(By.CLASS_NAME,'main-value')
    return rrp.text

def findCategory(prodUrl):
    catList = []
    driver.set_page_load_timeout(30) 
    driver.get(prodUrl)
    catList = driver.find_elements(By.itemprop,'name')
    return catList

for index, row in dfCef.iterrows():
    dfCef.loc[index,'rrp'] = rrpFunction(dfCef.loc[index,'Link'])
    dfCef.loc[index,'CEF Category'] = findCategory(dfCef.loc[index,'Link'])

dfCef.to_excel('cefScraping v2.xlsx', index=False)