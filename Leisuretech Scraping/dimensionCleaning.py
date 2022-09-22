import pandas as pd
import re

dfLeisureTec = pd.read_excel('LeisureTec v2.xlsx')
weightList = dfLeisureTec['Weight'].tolist()

for cell in weightList:
        try:
                kgEndIndex = re.search('kg', cell)
                print(cell)
                while True:
                        counter = kgEndIndex.span()[0]
                        print(cell[counter])
                        if cell[counter].isdigit() or cell[counter] == '.':
                                counter -= 1
                        else:
                                break
                #print(str(counter) + ' and ' + str(kgEndIndex.span()[0]))
                weight = cell[counter:kgEndIndex.span()[0]]
                print(weight)              
        except:
                pass


