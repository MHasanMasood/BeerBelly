from pattern.web import URL, Document, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from pattern.web import abs

import json
import csv


beerData = open("beerData.csv", 'w')
classPullList = ["BAscore_big ba-score","ba-score_text","ba-ratings","BAscore_big ba-bro_score","ba-bro_text","ba-reviews","ba-ravg","ba-pdev"]
fields = ["Beer Style", "Beer Name"] + classPullList
beerWriter = csv.writer(beerData)
beerWriter.writerow(fields)

mainSite = "http://www.beeradvocate.com"
query = '?start='

url = URL('http://www.beeradvocate.com/beer/style/')
domMain = Document(url.download(Cache=True))
tableMain = domMain.by_tag('table')[0]
beerStyles = tableMain.by_tag('a')

for eachStyle in beerStyles:
    styleURLString = mainSite + eachStyle.attributes['href']
    styleURL = URL(styleURLString)
    
    domStyle = Document(styleURL.download())
    styleTable = domStyle.by_tag('table')
    
    howMany = styleTable[0].by_tag('b')[0].content.split()
    howManyInt = int(howMany[8].replace(")",""))     
    queryList = range(0,howManyInt,50)
    
    for eachQuery in queryList:
        beerStyleQuery = URL(styleURLString+query+str(eachQuery))
        beerStyleTable = Document(beerStyleQuery.download()).by_tag('table')[0]
        beerStyleTableRows = beerStyleTable.by_tag('tr')
        del beerStyleTableRows[0]
        del beerStyleTableRows[0]
        del beerStyleTableRows[0]
        del beerStyleTableRows[len(beerStyleTableRows)-1]
        for row in beerStyleTableRows:
            beerBit = row.by_tag('a')[0]
            beerName = beerBit.by_tag('b')[0].content
            beerURL = URL(mainSite + beerBit.attributes['href'])
            beerDOM = Document(beerURL.download())
            eachLine = [eachStyle.content.encode('utf-8'), beerName.encode('utf-8')]
            for aClass in classPullList:
                aField = beerDOM.getElementsByClassname(aClass)[0].content
                eachLine = eachLine + [aField.encode('utf-8')]
            beerWriter.writerow(eachLine)
                


beerData.close()
