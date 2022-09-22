from logging import exception
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from urllib.parse import urljoin
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from tqdm import tqdm

letterList = ['abc', 'def','ghi','jkl','mno','pqr','stu','vwx','yz']
shopUrl = 'https://www.midwich.com/technologies/manufacturers/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

dfMidwich = pd.DataFrame()

path = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.set_page_load_timeout(30)
driver.get(shopUrl)
'''links = driver.find_elements_by_class_name('js-brand-scroll')
for link in links:
    letterUrl = link.get_attribute('href')
    driver.get(letterUrl)'''
links = driver.find_elements(By.CLASS_NAME, '"brands__list')
for link in links:
    driver.set_page_load_timeout(30)
    driver.get(link.get_atrribute('href'))
    productList = driver.find_elements(By.CLASS_NAME, 'tile-compare')
    for product in productList:
        print(product.get_attribute('href'))
    
