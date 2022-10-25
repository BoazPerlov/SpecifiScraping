from inspect import getmembers
import pandas as pd
import re


dfPolar = pd.read_excel('Polar Audio scraping.xlsx')

def getMes(measure):
    print(measure)

for index, row in dfPolar.iterrows():
    specs = dfPolar.loc[index,'specs']
    HWD = []
    if not pd.isnull(dfPolar.loc[index,'specs']):
        mesWithSpace = re.findall('([0-9]+) ?x ?([0-9]+) ?x ?([0-9]+) ? mm', specs)
        mesWithoutSpace = re.findall('([0-9]+) ?x ?([0-9]+) ?x ?([0-9]+) ?mm', specs)
        mesInd = re.findall('([0-9]+) ?mm', specs)
        dfPolar.loc[index,'with'] = str(mesWithSpace)
        dfPolar.loc[index,'without'] = str(mesWithoutSpace)
        dfPolar.loc[index,'ind'] = str(mesInd)
        mesDict = {'withSpaces': mesWithSpace,'Without Spaces':mesWithoutSpace, 'Ind':mesInd}

    
'''    try:
        mesDict = {'heightW':mesWithSpace[0][0],'widthW':mesWithSpace[0][1],'depthW':mesWithSpace[0][2],'heightWO':mesWithoutSpace[0][0],'widthWO':mesWithoutSpace[0][1],'depthWO':mesWithoutSpace[0][2]}
        dfPolar = dfPolar.append(mesDict, ignore_index=True)
    except:
        print('dfsdf')


               if mesWithSpace:
            dfPolar.loc[index,'Full measurement'] = mesWithSpace
        elif mesWithoutSpace:
            dfPolar.loc[index,'Full measurement'] = mesWithoutSpace
        elif mesInd:
            print(mesInd)
            dfPolar.loc[index,'Full measurement'] = mesInd[0]
'''

    



dfPolar.to_excel('Polar Audio Scraping v2.xlsx', index=False)