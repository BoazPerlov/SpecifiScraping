from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from datetime import datetime
from tqdm import tqdm


dfAbility = pd.DataFrame()
originalUrl = 'https://www.ability-av.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

#path = "C:/Program Files (x86)/chromedriver.exe"
#driver = webdriver.Chrome(path)

abilitySoup = bs(requests.get(originalUrl).text,'lxml')
catagoryLinks = abilitySoup.find_all('a',{'class':'cat'})
for link in tqdm(catagoryLinks):
    categorySoup = bs(requests.get('https://www.ability-av.com/'+link['href']).text,'lxml')
    productLinks = categorySoup.find_all('td',{'class':'item'})
    for productLink in productLinks:
        mainLink = productLink.findChild('a')['href']
        productSoup = bs(requests.get('https://www.ability-av.com/'+mainLink).text,'lxml')
        productName = productSoup.find_all('td',{'class':'page_headers'})
        mpns = productSoup.find_all('strong')

