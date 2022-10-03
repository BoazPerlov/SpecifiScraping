
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
path = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(path)


cefSoup = bs(requests.get((originalUrl)).text,'lxml')
catLists = cefSoup.find_all('a',{'class':'divider-vertical'})
for catList in tqdm(catLists):
    for i in range(1,5):
        catUrl = catList['href'] + '?page=' + str(i)
        subCatSoup = bs(requests.get(catUrl).text,'lxml')
        subCatList = subCatSoup.find_all('div',{'class':'top_level'})
        for subCat in subCatList:
            for j in range(1,10):
                productPageUrl = subCat.findChild('a')['href'] + '?page='+str(i)
                driver.set_page_load_timeout(30)
                driver.get(productPageUrl)
                productLinks = driver.find_elements(By.CLASS_NAME, 'product-listings__image-wrapper')
                for productLink in productLinks:
                    brand = ''
                    weight = ''
                    warranty = ''
                    description = ''
                    color = ''
                    length = ''
                    diameter = ''
                    productSoup = bs(requests.get(productLink.get_attribute('href')).text,'lxml')
                    link = productLink.get_attribute('href')
                    mpn = productSoup.find('ul',{'class','product-codes'}).findChild('strong').get_text()
                    sku = productSoup.find('ul',{'class','product-codes'}).findChild('li').find_next_sibling().findChild('strong').get_text()          
                    productName = productSoup.find('h1',{'class','details_page'}).get_text()
                    images = productSoup.find_all('img',{'class':'product-image'})
                    imageList = []
                    featuresList = productSoup.find('ul',{'class','product-features'}).findChildren('li')
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
                            if spec.get_text().strip() == 'Colour':
                                color = spec.find_next('td').get_text().strip()
                    dfCef = dfCef.append({'Link':link, 'brand':brand, 'productName':productName,'mpn':mpn, 'description':description, 'image':imageList, 'weight':weight, 'sku':sku,'Warranty':warranty, 'Colour':color, 'Diameter':diameter, 'Length':length}, ignore_index=True)
                dfCef.to_excel('cefScraping.xlsx',index=False) 
dfCef.to_excel('cefScraping.xlsx',index=False) 









'''productUrl = subCat.findChild('a')['href']
productHtml = requests.get(productUrl)
productSoup = bs(productHtml.text,'lxml')
productLink = productSoup.find_all('ul', {'class':'product-listings__codes'})
print(productLink)'''