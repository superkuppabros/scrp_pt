import re
import math
import json
import urllib.request, urllib.error, urllib.parse
import os
from bs4 import BeautifulSoup


def baseStrToZeroNumArr(baseStr):
    if(int(baseStr[-1], 36) <= 19):
        baseStr += 'l'
    baseStr = re.sub(r'[m-z]', 'l', baseStr.lstrip('k'))

    resArr = []
    tempArr = baseStr.split('k')
    if(len(tempArr[0]) == 0):
        tempArr.pop(0)
    for str in tempArr:
        arr = str.split('l')
        overL = len(arr) - 2
        zeros, ones = str.split('l')[:2]
        zerosNum = 1 if len(zeros) == 0 else int(zeros, 20)
        resArr.append(zerosNum)
        if (overL > 0): resArr.extend([0] * overL)
        if(ones and len(ones) != 0):
            onesNum = int(ones, 20) - 1
            resArr.extend([0] * onesNum)

    return resArr


def convertZeroNumArr(zeroNumArr):
    dataLength = sum(zeroNumArr) + len(zeroNumArr) - 1
    if(dataLength == 69120):
        blockSize = 96
    elif(dataLength == 23040):
        blockSize = 32
    else:
        raise Exception("Decoded data size is not right.")

    zeroNumArr.pop()
    resArr = [[] for i in range(9)]
    counter = 0
    for value in zeroNumArr:
        counter += value
        position = counter // 9 if blockSize == 96 else math.floor(
            counter / 9) * 3
        lane = counter % 9
        resArr[lane].append(position)
        counter += 1
    return [
        counter,
        resArr[3],
        resArr[0],
        resArr[1],
        resArr[2],
        resArr[4],
        resArr[6],
        resArr[7],
        resArr[8],
        resArr[5],
    ]


def convertedArrToSaveData(convertedArr):
    blockSize = 96
    maxNum = convertedArr.pop(0)
    maxPageNum = maxNum // 9 // blockSize + 1
    keyKind, keyNum = ('9B', 9) if max(
        convertedArr[0], convertedArr[8]) else ('7', 7)
    if(keyNum == 7):
        convertedArr = convertedArr[1:8]

    scores = [{
        'speeds': [],
        'notes': [[] for i in range(keyNum)],
        'freezes': [[] for i in range(keyNum)]
    } for j in range(maxPageNum)]

    for lane, laneArr in enumerate(convertedArr):
        for position in laneArr:
            page = position // blockSize
            pos = (position % blockSize) * 4
            scores[page]['notes'][lane].append(pos)

    obj = {
        'blankFrame': 200,
        'timings': [
            {
                'label': 1,
                'startNum': 0,
                'bpm': 140,
            },
        ],
        'scoreNumber': 1,
        'scores': scores,
        'keyKind': keyKind,
    }

    return json.dumps(obj)


def makeSaveData(baseStr):
    zeroNumArr = baseStrToZeroNumArr(baseStr)
    convertedArr = convertZeroNumArr(zeroNumArr)
    saveData = convertedArrToSaveData(convertedArr)
    return saveData

def getStageData(id):
    url = "http://popntube.com/popntube2.php?d0=" + str(id)
    html = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")[1]
    return scripts.contents[0]

def writeSaveData(id):
    os.makedirs(f'save', exist_ok=True)
    source = getStageData(id)
    pattern = re.compile(r'var stageData=\'([0-9a-z]+)\'')
    stageData = pattern.search(source).group(1)
    saveData = makeSaveData(stageData)
    f = open(f'save/{id}.json', "w")
    f.write(saveData)
    f.close()


id = input('input stage id: ')
writeSaveData(id)
