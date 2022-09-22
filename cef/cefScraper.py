
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from tqdm import tqdm

originalUrl = 'https://www.cef.co.uk/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
dfCef = pd.DataFrame()


cefSoup = bs(requests.get((originalUrl)).text,'lxml')
catLists = cefSoup.find_all('a',{'class':'divider-vertical'})
for catList in catLists:
    for i in range(1,5):
        catUrl = catList['href'] + '?page=' + str(i)
        subCatSoup = bs(requests.get(catUrl).text,'lxml')
        subCatList = subCatSoup.find_all('div',{'class':'top_level'})
        for subCat in subCatList:
            print(subCat.findChild('a')['href'])

