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

docTitle = ['User Guide','Brochure','Datasheet','Settings']
dfMartinAudio = pd.DataFrame()

originalUrl = 'https://martin-audio.com/products'
shopSoup = bs(requests.get(originalUrl).text,'lxml')
productLinks = shopSoup.find_all('div', {'class':'product-block'})
for productLink in productLinks:
    docLinks = []
    imageList = []
    specDict = {}
    description = ''
    pLink = productLink.findChild('a')['href']
    productSoup = bs(requests.get(pLink).text,'lxml')

    images = productSoup.find_all('img', {'class':'lazyloaded'})
    for image in images:
        imageList.append(image['href'])
    productName = productSoup.find('div',{'id':'breadcrum'}).findChildren('li')[-1].get_text()
    try:
        description = productSoup.find('p',{'class':'lead'}).get_text()
    except:
        pass
    docList = productSoup.find_all('a')
    for doc in docList:
        try:
            if any(posTitle in doc['title'] for posTitle in docTitle):
                docLinks.append(doc['href'])
        except:
            pass
    
    try:
        specTable = productSoup.find('table',{'class':'specification-table'}).findChildren('tr')
        for spec in specTable:
            specs = spec.findChildren('td')
            specDict[specs[0].get_text()] = specs[1].get_text()
    except:
        pass
    productDict = {'Link':pLink,'Product Name':productName,'Description':description,'Images':imageList,'Documents':docLinks, 'Specifications':specDict}
    dfMartinAudio = dfMartinAudio.append(productDict, ignore_index=True)
    dfMartinAudio.to_excel('Martin Audio.xlsx', index=False)

    

