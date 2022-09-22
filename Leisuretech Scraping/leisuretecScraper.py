
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
dfLeisureTec = pd.DataFrame()

def scrapingLeisureProducts(url):
    image = ''
    manual = ''
    height = ''
    depth = ''
    weight = ''
    featureString = ""
    specString = ''
    description = ''
    prodUrl = 'https://www.leisuretec.co.uk' + url
    productHtml = requests.get((prodUrl))
    productSoup = bs(productHtml.text,'lxml')
    try:
        manual = 'https://www.leisuretec.co.uk' + productSoup.find('a',{'class':'product-page-information-attachments-list-item-link'})['href']
    except:
        pass
    try:
        image = 'https://www.leisuretec.co.uk' + productSoup.find('img',{'id':'main-img'})['src']
    except:
        pass
    try:
        tabThree = productSoup.find('div', {'id':'tab-3'}).findChildren('li')
        for spec in tabThree:
            specString += '\n' + spec.get_text()
            if re.search("^Weight", spec.get_text()):
                weight = spec.get_text().replace('Weight: ',"")
            if re.search("^Height:", spec.get_text()):
                height = spec.get_text().replace('Height: ',"")
            if re.search("^Depth", spec.get_text()):
                depth = spec.get_text().replace('Depth: ',"").replace('Depth (incl front): ','')
    except:
        pass
    try:
        tabTwo = productSoup.find('div',{'id':'tab-2'}).findChildren('li')
        for feature in tabTwo:
            featureString += '\n' + feature.get_text()
    except Exception as e:
        pass
    try:
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
    except:
        pass
    scrapDict = {'Link':'https://www.leisuretec.co.uk' + product['href'], 'brand':productBrand, 'productName':productName,'RRP':rrp, 'mpn':mpn, 'Description':description,'image':image, 'manual':manual, 'specs': specString, 'features':featureString, 'Weight':weight,'Height':height, 'Depth':depth}
    return scrapDict

for category in categoryList:
    shopUrl = originalUrl + category
    shopHtml = requests.get(shopUrl)
    bSoup = bs(shopHtml.text,'lxml')
    subCategories = bSoup.find_all('a',{'class':'listing-link'})
    for subCat in subCategories[::2]:
        subCatHtml = requests.get('https://www.leisuretec.co.uk' + subCat['href'])
        print('the sub category is ' + subCat['href'])
        subCatSoup = bs(subCatHtml.text,'lxml')
        subSubCategories = subCatSoup.find_all('a',{'class':'listing-link'})
        for subSubCat in tqdm(subSubCategories[::2]):
            subSubHtml = requests.get('https://www.leisuretec.co.uk' + subSubCat['href'])
            #print('the subsub category is ' + subSubCat['href'])
            subSubSoup = bs(subSubHtml.text,'lxml')
            productPages = subSubSoup.find_all('a',{'class':'pagination-link'})
            paginationLinks = []
            for productPage in productPages:
                #print(paginationLinks)
                if 'per_page' in productPage['href']:
                    pass
                elif 'sort' not in productPage['href'] and productPage['href'] not in paginationLinks:
                    subCatLink = requests.get('https://www.leisuretec.co.uk' + productPage['href'])
                    #print('the product page is ' + productPage['href'])
                    paginationLinks.append(productPage['href'])
                    subCatSoup = bs(subCatLink.text,'lxml')
                    products = subCatSoup.find_all('a',{'class':'product-page-link'})
                    for product in products[::2]:
                        #print('the product is ' + product['href'])
                        dfLeisureTec = dfLeisureTec.append(scrapingLeisureProducts(product['href']), ignore_index=True)
        dfLeisureTec.to_excel('LeisureTec v2.xlsx',index=False)
            
dfLeisureTec.to_excel('LeisureTec v2.xlsx',index=False)

