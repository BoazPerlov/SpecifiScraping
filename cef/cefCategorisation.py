from itertools import product
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

dfCef = pd.read_excel('cefScraping Updated.xlsx')

for index, row in tqdm(dfCef.iterrows()):
    spanList = []
    link = dfCef.loc[index,'Link']
    productSoup = bs(requests.get(link).text,'lxml')
    allSpans = productSoup.find('div',{'id':'breadcrumbs'}).findChildren('span')
    for span in allSpans:
        spanList.append(span.get_text().strip())
    dfCef.loc[index,'Breadcrumbs'] = str(spanList)

dfCef.to_excel('cef Scraping Categorised.xlsx', index=False)
