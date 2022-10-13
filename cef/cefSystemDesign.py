import pandas as pd
from collections import defaultdict
from tqdm import tqdm

dfCef = pd.read_csv('cef Scraping Categorised v2.csv')

catDict = defaultdict(list)
mainCategories = set(dfCef['Breadcrumbs'].to_list())

for index, row in tqdm(dfCef.iterrows()):
    for mainCategory in mainCategories:
        if dfCef.loc[index,'Breadcrumbs'] == mainCategory:
            catDict[mainCategory].append(dfCef.loc[index,'Breadcrumbs 2'])

for key, value in catDict.items():
    catDict[key] = list(set(catDict[key]))

for index, row in tqdm(dfCef.iterrows()):
    if dfCef.loc[index,'Breadcrumbs'] == "Cables and IR":
        dfCef.loc[index,'Category'] = "Cables and IR"
        if dfCef.loc[index,'Breadcrumbs 2'] == ' Cable Accessories':
            dfCef.loc[index,'System Design'] = '{"cableType":"' + dfCef.loc[index,'Breadcrumbs 3']+'"}'
        elif 'CAT' in dfCef.loc[index,'Breadcrumbs 2']:
            dfCef.loc[index,'System Design'] = '{"cableType":"CAT6 Cables"}'
        else:
            dfCef.loc[index,'System Design'] = '{"cableType":"Power Cables"}'
    elif dfCef.loc[index,'Breadcrumbs'] == " Cable Management":
        dfCef.loc[index,'Category'] = "Cable Management"
        dfCef.loc[index,'System Design'] = '{"cableManagementType":"' + dfCef.loc[index,'Breadcrumbs 2']+'"}'
    elif dfCef.loc[index,'Breadcrumbs'] == " Wiring Accessories":
        dfCef.loc[index,'Category'] = "Accessories"
        dfCef.loc[index,'System Design'] = '{"accessoryType":"Other"}'
    elif dfCef.loc[index,'Breadcrumbs'] == " Tools":
        dfCef.loc[index,'Category'] = "Accessories"
        dfCef.loc[index,'System Design'] = '{"accessoryType":"' + dfCef.loc[index,'Breadcrumbs 3']+'"}'
    elif dfCef.loc[index,'Breadcrumbs'] == " Test Equipment" or dfCef.loc[index,'Breadcrumbs'] == ' Power Tools':
        dfCef.loc[index,'Category'] = "Accessories"
        dfCef.loc[index,'System Design'] = '{"accessoryType":"Tools"}'
    elif dfCef.loc[index,'Breadcrumbs'] == " Switchgear & Distribution" or dfCef.loc[index,'Breadcrumbs'] == " Industrial Controls" or dfCef.loc[index,'Breadcrumbs'] == " Domestic & Smart Home":
        dfCef.loc[index,'Category'] = "Electrical"
        dfCef.loc[index,'System Design'] = '{"electricalType":"' + dfCef.loc[index,'Breadcrumbs 2']+'"}'
    elif dfCef.loc[index,'Breadcrumbs'] == " Lighting Luminaires" or dfCef.loc[index,'Breadcrumbs'] == " Lamps & Tubes":
        dfCef.loc[index,'Category'] = "Lighting"
        dfCef.loc[index,'System Design'] = '{"lightingType":"LED Fixtures"}'
    elif dfCef.loc[index,'Breadcrumbs'] == " Heating & Ventilation":
        dfCef.loc[index,'Category'] = "Climate"



dfCef.to_csv('cef Scraping Categorised v3.csv',index=False)
