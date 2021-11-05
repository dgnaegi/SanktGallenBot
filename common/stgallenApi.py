from urllib.request import urlopen
import json

stGallenAPIURL = "https://daten.stadt.sg.ch/api/records/1.0/search/?dataset="

def getAPIRecords(dataSetName):
    url = stGallenAPIURL + dataSetName
    records = json.load(urlopen(url))['records']
    return records