
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from tqdm import tqdm

dfLeisureTec = pd.read_excel('LeisureTec.xlsx')
dfNew = pd.DataFrame()
linkList = dfLeisureTec['Link'].tolist()

for link in tqdm(linkList):
        height = ''
        depth = ''
        weight = ''
        manual = ''
        image = ''
        featureString = ''
        specString = ''
        productHtml = requests.get(link)
        productSoup = bs(productHtml.text,'lxml')
        try:
            manual = 'https://www.leisuretec.co.uk' + productSoup.find('a',{'class':'product-page-information-attachments-list-item-link'})['href']
            image = 'https://www.leisuretec.co.uk' + productSoup.find('img',{'id':'main-img'})['src']
        except Exception as e:
            print(e)
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
            tabTwo = productSoup.find('div',{'id':'tab-2'}).findChildren('li')
            
            for feature in tabTwo:
                featureString += '\n' + feature.get_text()
        except Exception as e:
            print(e)

        scrapDict = {'Link':link, 'brand':productBrand, 'productName':productName,'RRP':rrp, 'mpn':mpn, 'Description':description,'image':image, 'manual':manual, 'specs': specString, 'features':featureString, 'Weight':weight,'Height':height, 'Depth':depth}
        dfNew = dfNew.append(scrapDict, ignore_index=True)
        dfNew.to_excel('LeisureTec v3.xlsx',index=False)

dfNew.to_excel('LeisureTec v3.xlsx',index=False)
