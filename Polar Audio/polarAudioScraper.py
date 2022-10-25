
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


dfPolar = pd.DataFrame()
originalUrl = 'https://polar.uk.com/online-shop/brands'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

#path = "C:/Program Files (x86)/chromedriver.exe"
#driver = webdriver.Chrome(path)

polarSoup = bs(requests.get(originalUrl).text,'lxml')
brandLinks = polarSoup.find_all('a',{'class':'c-card__image-container'})
for link in tqdm(brandLinks):
    brandSoup = bs(requests.get('https://polar.uk.com/'+link['href']).text,'lxml')
    productLinks = brandSoup.find_all('a',{'class':'c-card__image-container'})
    for productLink in productLinks:
        docsList = []
        specs = []
        imageList = []
        link = 'https://polar.uk.com/'+productLink['href']
        productSoup = bs(requests.get(link).text,'lxml')
        brand = productSoup.find('span',{'class':'c-product-description__manufacturer'}).get_text()
        productName = productSoup.find('span',{'class':'c-product-description__product-name'}).get_text()
        skuData = productSoup.find_all('h5',{'class':'c-product-description__skucode'})
        for item in skuData:
            if 'SKU' in item.get_text():
                sku = item.get_text().replace('SKU: ','')
            elif 'UPC' in item.get_text():
                mpn = item.get_text().replace('UPC: ','')
        downloadList = productSoup.find_all('a',{'class':'c-card--download'})
        for dl in downloadList:
            docsList.append(dl['href'])
        description = productSoup.find('div',{'class':'c-product-description__description'}).findChild('p').get_text()
        specsList = productSoup.find_all('span',{'c-technical-specification__element-title'})
        for spec in specsList:
            if 'Dimensions' in spec.get_text():
                specs.append(spec.find_next_sibling('span').get_text())
                #print(spec.find_next_sibling('span').get_text())
        images= productSoup.find_all('img',{'c-product-details-slider__image'})
        for image in images:
            try:
                imageList.append(image['data-src'])
            except:
                imageList.append(image['src'])
        polarProductDict= {'Link':link, 'brand':brand, 'productName':productName,'mpn':mpn, 'docs':docsList,'description':description, 'image':imageList, 'sku':sku,'Warranty':'2 years', 'specs':specs}
        dfPolar = dfPolar.append(polarProductDict,ignore_index=True)

dfPolar.to_excel('Polad Audio scraping.xlsx', index=False)