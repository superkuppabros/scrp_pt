import urllib.request, urllib.error, urllib.parse
import os
from bs4 import BeautifulSoup

def createUrl(creator, diff):
    url = "http://popntube.com/index.php?register=" + creator
    url += "&diffFrom=" + str(diff)
    url += "&diffTo=" + str(diff + 1)
    return url

def getStageIdList(creator, diff):
    url = createUrl(creator, diff)
    html = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(html, "html.parser")
    stageList = soup.find_all("div", id = "stage")
    onClickList = [stage["onclick"] for stage in stageList]
    idList = [onClick.replace("stageClick(","").replace(")","") for onClick in onClickList]
    return idList

def getStageData(id):
    url = "http://popntube.com/popntube2.php?d0=" + str(id)
    html = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")[1]
    return scripts.contents[0]

def writeAllStageData(creator):
    os.makedirs(f'stage/{creator}', exist_ok=True)
    encodeCreator = urllib.parse.quote(creator)
    idList = sum([getStageIdList(encodeCreator, x) for x in range(0,30)],[])
    for id in idList:
        stageData = getStageData(int(id))
        f = open(f'stage/{creator}/{id}.js', "w")
        f.write(stageData)
        f.close()

creator = input("input creator's name: ")
writeAllStageData(creator)
