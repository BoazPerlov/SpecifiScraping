
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from tqdm import tqdm

categoryList = ['sound','lighting','special-effects','ancillary', 'video']
originalUrl = 'https://www.leisuretec.co.uk/category/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
#path = "C:/Program Files (x86)/chromedriver.exe"
#driver = webdriver.Chrome(path)

dfLeisureTec = pd.DataFrame()

for category in categoryList:
    shopUrl = originalUrl + category
    shopHtml = requests.get(shopUrl)
    bSoup = bs(shopHtml.text,'lxml')
    subCategories = bSoup.find_all('a',{'class':'listing-link'})
    for subCat in tqdm(subCategories):
        subCatHtml = requests.get('https://www.leisuretec.co.uk' + subCat['href'])
        subCatSoup = bs(subCatHtml.text,'lxml')
        subSubCategories = subCatSoup.find_all('a',{'class':'listing-link'})
        try:
            for subSubCat in subSubCategories:
                subSubHtml = requests.get('https://www.leisuretec.co.uk' + subSubCat['href'])
                subSubSoup = bs(subSubHtml.text,'lxml')
                products = subSubSoup.find_all('a',{'class':'product-page-link'})
                for product in products:
                    prodUrl = 'https://www.leisuretec.co.uk' + product['href']
                    productHtml = requests.get(('https://www.leisuretec.co.uk' + product['href']))
                    #driver.set_page_load_timeout(30)
                    #driver.get(prodUrl)
                    productSoup = bs(productHtml.text,'lxml')
                    manual = productSoup.find('a',{'class':'product-page-information-attachments-list-item-link'})['href']
                    image = 'https://www.leisuretec.co.uk' + productSoup.find('img',{'id':'main-img'})['src']
                    rrp = productSoup.find('div',{'class':'product-page-price'}).get_text()
                    brands = productSoup.find_all('dt')
                    for brand in brands:
                        if 'Brand' in brand.get_text():
                            productBrand = brand.find_next('dd').get_text()
                        if 'Code' in brand.get_text():
                            mpn = brand.find_next('dd').get_text()
                    nameDivs = productSoup.find_all('div', {'class':'col-xs-12'})
                    for nameDiv in nameDivs:
                        if nameDiv.findChild('h1'):
                            productName = nameDiv.findChild('h1').get_text()
                    descDiv = productSoup.find('div', {'class':'product-page-information-bulletpoints-container'}).findChild('ul')
                    description = descDiv.get_text()
                    #specDiv = productSoup.find('div', {'class':'product-page-tabs-tab-pane-container'}).findChild('ul')
                    #specs = specDiv.get_text()
                    #manualLink = productSoup.find('a',{'class':'product-page-information-attachments-list-item-link'})['href']
                    #print(productSoup.find_all('li',{'class':'product-page-tabs-list-item'})['href'])
                    scrapDict = {'Link':'https://www.leisuretec.co.uk' + product['href'], 'brand':productBrand, 'productName':productName,'RRP':rrp, 'mpn':mpn, 'Description':description,'image':image, 'manual':manual}
                    dfLeisureTec = dfLeisureTec.append(scrapDict, ignore_index=True)
                    dfLeisureTec.to_excel('LeisureTec v2.xlsx',index=False)
                
        except Exception as e:
            print(e)
            continue
dfLeisureTec.to_excel('LeisureTec v2.xlsx',index=False)

