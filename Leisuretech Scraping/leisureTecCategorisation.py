from tqdm import tqdm
import pandas as pd

dfLT = pd.read_excel('LeisureTec v7.xlsx')

def weightfinder(cell):
    kgStartIndex = cell.find('kg')
    counter = kgStartIndex-1
    while True:
        if cell[counter].isdigit() or cell[counter] == '.':
            counter = counter-1
        else:
            break
    return cell[counter+1:kgStartIndex]

def poundCoverter(cell):
    lbStartIndex = cell.find('lb')
    counter = lbStartIndex -1
    while True:
        if cell[counter].isdigit() or cell[counter] == '.':
            counter = counter-1
        else:
            break
    if cell[counter+1:lbStartIndex].isdigit and cell[counter+1:lbStartIndex]:
        return cell[counter+1:lbStartIndex]

def inchesToCm(cell):
    incStartIndex = cell.find('"')
    counter = incStartIndex-1
    try:
        while True:
            if cell[counter].isdigit() or cell[counter] == '.':
                counter = counter-1
            else:
                break
    except:
        pass
    if cell[counter+1:incStartIndex].isdigit:
            return cell[counter+1:incStartIndex]

def mmmmm(cell):
    incStartIndex = cell.find('mm')
    if incStartIndex != -1:
        counter = incStartIndex-1
        try:
            while True:
                if cell[counter].isdigit() or cell[counter] == '.':
                    counter = counter-1
                else:
                    break
        except:
            pass
        if cell[counter+1:incStartIndex].isdigit:
                return cell[counter+1:incStartIndex]

def ggg(cell):
    incStartIndex = cell.find('g')
    if incStartIndex != -1:
        counter = incStartIndex-1
        try:
            while True:
                if cell[counter].isdigit() or cell[counter] == '.':
                    counter = counter-1
                else:
                    break
        except:
            pass
        if cell[counter+1:incStartIndex].isdigit:
                return cell[counter+1:incStartIndex]

for index, row in dfLT.iterrows():
    dfLT.loc[index,'New Weight'] = ggg(str(dfLT.loc[index,'Weight']))
    
dfLT.to_excel('LeisureTec v8.xlsx', index=False)