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
links = driver.find_elements_by_class_name('js-brand-scroll')


shopHtml = requests.get(shopUrl)
bSoup = bs(shopHtml.text,'lxml')
letterList = bSoup.find_all('a',{'class':'js-brand-scroll'})
for letter in letterList:
    print(letter['href'])
    letterUrl = 'https://www.midwich.com/' + letter['href']
    letterHtml = requests.get(letterUrl)
    letterSoup = bs(letterHtml.text,'lxml')
    brandList = letterSoup.find_all("div", {"class": "brands__list"})
    for blist in brandList:
        brands = blist.findChildren('a')
        for brand in brands:
            if 'brand' in brand['href']:
                print(brand['href'])
                brandHtml = requests.get(brand['href'])
                brandName = brand['href'].split('/')[-1]
                brandSoup = bs(brandHtml.text,'lxml')
                paging = brandSoup.find('ul', {'class':'pagination'})
                if paging:
                    for i in range(30):
                        brandHtml = requests.get(brand['href'] + '/' +str(i))
 
                        brandSoup = bs(brandHtml.text,'lxml')
                        productList = brandSoup.find_all("a", {"class": "tile-compare"})
                        for product in productList:
                            productHtml = requests.get('https://store.midwich.com' + product['href'])
                            productSoup = bs(productHtml.text,'lxml')
                            productName = product['href'].split('/')[3]
                            rrp = productSoup.find('p', {'class':'rrp'}).get_text().strip().replace('RRP:','')
                            divList = productSoup.find_all('div', {'class':'col-md-7'})
                            for div in divList:
                                divC = div.findChildren('strong')
                                mpn = divC[0].get_text().replace('N/A',"")
                            try:
                                description1 = productSoup.find('div', {'class':'midwTruncate'}).findChild('h4').get_text()
                                description2 = productSoup.find('div', {'class':'midwTruncate'}).findChild('p').get_text()
                                fullDescription = description1 + '\n' + description2
                                image = 'https://store.midwich.com' + productSoup.find('img',{'class':'product-image HD1080'})['src']
                            except:
                                continue
                            features = productSoup.find_all('td',{'class':'feature'})
                            for feature in features:
                                if 'Dimensions' in feature.get_text():
                                    dimensions = feature.find_next('td').text.strip()
                                if 'Weight' in feature.get_text():
                                    weight = (feature.find_next('td').text.strip().replace('kg',""))
                            dfMidwich = dfMidwich.append({'Link':'https://store.midwich.com' + product['href'], 'brand':brandName, 'productName':productName,'RRP':rrp, 'mpn':mpn, 'Description':fullDescription,'image':image, 'dimensions':dimensions,'weight':weight}, ignore_index=True)
                            dfMidwich.to_excel('test1.xlsx',index=False) 
                else:
                    productList = brandSoup.find_all("a", {"class": "tile-compare"})
                    for product in productList:
                        productHtml = requests.get('https://store.midwich.com' + product['href'])
                        productSoup = bs(productHtml.text,'lxml')
                        productName = product['href'].split('/')[3]

                        rrp = productSoup.find('p', {'class':'rrp'}).get_text().strip().replace('RRP:','')
                        divList = productSoup.find_all('div', {'class':'col-md-7'})
                        for div in divList:
                            divC = div.findChildren('strong')
                            mpn = divC[0].get_text().replace('N/A',"")
                        try:
                            description1 = productSoup.find('div', {'class':'midwTruncate'}).findChild('h4').get_text()
                            description2 = productSoup.find('div', {'class':'midwTruncate'}).findChild('p').get_text()
                            fullDescription = description1 + '\n' + description2
                            image = 'https://store.midwich.com' + productSoup.find('img',{'class':'product-image HD1080'})['src']
                        except:
                            continue

                        features = productSoup.find_all('td',{'class':'feature'})
                        for feature in features:
                            if 'Dimensions' in feature.get_text():
                                dimensions = feature.find_next('td').text.strip()
                            if 'Weight' in feature.get_text():
                                weight = (feature.find_next('td').text.strip().replace('kg',""))
                        dfMidwich = dfMidwich.append({'Link':'https://store.midwich.com/' + product['href'], 'brand':brandName, 'productName':productName,'RRP':rrp, 'mpn':mpn, 'Description':fullDescription,'image':image, 'dimensions':dimensions,'weight':weight}, ignore_index=True)
                        dfMidwich.to_excel('test1.xlsx',index=False)               


