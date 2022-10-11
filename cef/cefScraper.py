
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

doneCats = ['cables-and-accessories','cable-management','cctv-fire-security','data-networking','domestic-appliances','tools-fixings','heating-ventilation','lamps-tubes','switchgear-distribution','lighting-luminaires','power-tools', 'test-equipment', 'tools-fixings', 'industrial-control']

dfOriginalCef = pd.read_excel('cefScraping Updated.xlsx')
linkList = dfOriginalCef['Link'].to_list()
originalUrl = 'https://www.cef.co.uk/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
dfCef = pd.DataFrame()
path = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(path)

def directProductPage(productLink):
    mpn = ''
    sku = ''
    brand = ''
    productName = ''
    weight = ''
    warranty = ''
    description = ''
    color = ''
    length = ''
    diameter = ''
    height = ''
    width = ''
    docsList = []
    featuresList = []
    productSoup = bs(requests.get(productLink.get_attribute('href')).text,'lxml')
    link = productLink.get_attribute('href')
    if link not in linkList:
        try:
            mpn = productSoup.find('ul',{'class','product-codes'}).findChild('strong').get_text()
            sku = productSoup.find('ul',{'class','product-codes'}).findChild('li').find_next_sibling().findChild('strong').get_text()   
            productName = productSoup.find('h1',{'class','details_page'}).get_text()
            featuresList = productSoup.find('ul',{'class','product-features'}).findChildren('li')       
        except:
            pass
        images = productSoup.find_all('img',{'class':'product-image'})
        imageList = []
        docs = productSoup.find_all('a',{'class':'download_tracker'})
        for doc in docs:
            docsList.append(doc['href'])
        for feature in featuresList:
            description += feature.get_text() + '\n'
        for image in images:
            imageList.append(image['src'])
        specTable = productSoup.find('div',{'class','spec-table'}).findChildren('td')
        for spec in specTable:
            if 'Brand' in spec.get_text():
                brand = spec.find_next('td').get_text().strip()
            if 'Weight' in spec.get_text():
                weight = spec.find_next('td').get_text().strip()
            if 'Guarantee' in spec.get_text():
                warranty = spec.find_next('td').get_text().strip()
            if 'Length' in spec.get_text():
                length = spec.find_next('td').get_text().strip()
            if 'Diameter' in spec.get_text():
                diameter = spec.find_next('td').get_text().strip()
            if 'Height' in spec.get_text():
                height = spec.find_next('td').get_text().strip()
            if 'Width' in spec.get_text():
                width = spec.find_next('td').get_text().strip()
            if spec.get_text().strip() == 'Colour':
                color = spec.find_next('td').get_text().strip()
        return {'Link':link, 'brand':brand, 'productName':productName,'mpn':mpn, 'docs':docsList,'description':description, 'Width':width, 'Height':height, 'image':imageList, 'weight':weight, 'sku':sku,'Warranty':warranty, 'Colour':color, 'Diameter':diameter, 'Length':length}

cefSoup = bs(requests.get((originalUrl)).text,'lxml')
catLists = cefSoup.find_all('a',{'class':'divider-vertical'})
for catList in tqdm(catLists):
    #if not any(ele in catList['href'] for ele in doneCats):
        for i in range(1,25):
            catUrl = catList['href'] + '?page=' + str(i)
            subCatSoup = bs(requests.get(catUrl).text,'lxml')
            subCatList = subCatSoup.find_all('div',{'class':'top_level'})
            for subCat in subCatList:
                for l in range(1,25):
                    ncLink = subCat.findChild('a')['href'] + '?page=' + str(l)
                    nextCategorySoup = bs(requests.get(ncLink).text,'lxml')
                    nextCategories = nextCategorySoup.find_all('div', {'class':'product_category_image'})
                    if nextCategories:
                        for nextCategory in nextCategories:
                            for j in range(1,25):
                                productPageUrl = nextCategory.findChild('a')['href'] + '?page='+str(j)
                                nextNextCategoriesSoup = bs(requests.get(productPageUrl).text,'lxml')
                                nextNextCategories = nextNextCategoriesSoup.find_all('div', {'class':'product_category_image'})
                                if nextNextCategories:
                                    for nextnextCat in nextNextCategories: 
                                        for k in range(1,25):
                                            productPageUrl = nextnextCat.findChild('a')['href'] + '?page='+str(k)
                                            driver.set_page_load_timeout(30)
                                            driver.get(productPageUrl)
                                            productLinks = driver.find_elements(By.CLASS_NAME, 'product-listings__image-wrapper')
                                            for productLink in productLinks:
                                                productDict = directProductPage(productLink)
                                                dfCef = dfCef.append(productDict, ignore_index=True)
                                else:
                                    driver.set_page_load_timeout(30)
                                    driver.get(productPageUrl)
                                    productLinks = driver.find_elements(By.CLASS_NAME, 'product-listings__image-wrapper')
                                    for productLink in productLinks:
                                        productDict = directProductPage(productLink)
                                        dfCef = dfCef.append(productDict, ignore_index=True)
                            dfCef.to_excel('cefScraping.xlsx',index=False) 
                    else:
                        for j in range(1,25):
                            productPageUrl = subCat.findChild('a')['href'] + '?page='+str(j)
                            driver.set_page_load_timeout(30)
                            driver.get(productPageUrl)
                            productLinks = driver.find_elements(By.CLASS_NAME, 'product-listings__image-wrapper')
                            for productLink in productLinks:
                                productDict = directProductPage(productLink)
                                dfCef = dfCef.append(productDict, ignore_index=True)
                        dfCef.to_excel('cefScraping.xlsx',index=False) 


