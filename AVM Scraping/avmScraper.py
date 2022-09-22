import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import requests

dfNew = pd.DataFrame()
avmUrl = 'https://trade.avmltd.co.uk/all?per_page=168&page='
for i in range(1,22):
        print(i)
        pageUrl = 'https://trade.avmltd.co.uk/all?per_page=168&page=' + str(i)
        pageHtml = requests.get(pageUrl)
        pageSoup = bs(pageHtml.text,'lxml')
        products = pageSoup.find_all('a',{'class':'anchor'})
        for product in tqdm(products):
                features = []
                manual = ''
                image = ''
                productUrl = product['href']
                productHtml = requests.get(productUrl)
                productSoup = bs(productHtml.text,'lxml')
                try:
                        manual = productSoup.find('div',{'class':'documents-tab-content'}).findChild('a')['href']
                except:
                        pass
                try:
                        image = productSoup.find('img',{'id','image-zoom-main'})['src']
                except:
                        pass
                try:
                        productName = productSoup.find('h1',{'class','card-header'}).get_text()
                except:
                        pass
                try:
                        rrp = productSoup.find('span',{'class','net price'}).get_text()
                except:
                        pass
                try:
                        description = productSoup.find('div',{'class','short-description'}).get_text()
                except:
                        pass
                
                try:
                        productFeatures = productSoup.find('div',{'class','feature-row'}).findChildren('li')
                        for feature in productFeatures:
                                features.append(feature.get_text())
                except:
                        pass
                scrapDict = {'Link':product['href'], 'features':features, 'productName':productName,'RRP':rrp, 'Description':description,'image':image, 'manual':manual}
                dfNew = dfNew.append(scrapDict, ignore_index=True)
        dfNew.to_excel('AVM.xlsx',index=False)
dfNew.to_excel('AVM.xlsx',index=False)
		
