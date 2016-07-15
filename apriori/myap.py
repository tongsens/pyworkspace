__author__ = 'Administrator'

from getdata.getdata import *
import os

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def loadData(num=1000):
    gd = GetData()
    api_list,clss_list,md5_list = gd.getapidata(num)
    ret_list = []
    mal = u'malware'
    normal = u'normal'
    for i,data in enumerate(api_list):
        api = list(data.keys())
        if clss_list[i]>0:
            api.append(mal)
        else:
            api.append(normal)
        ret_list.append(api)
    volcablist = createVocabList(api_list)
    return ret_list, volcablist

def scanD(subset,D):
    count = 0
    for data in D:
        if subset.issubset(data):
            count += 1
    return count

def calcValue(xm, xn, xym, xyn):
    if xym==0 or xm==0:
        return 0
    if xyn==0 or xn==0:
        return 1
    return float(xym*xn)/float(xyn*xm)

def calcNext(starset,api_list ,D):
    M = set([u'malware'])
    N = set([u'normal'])
    for ss in starset:
        xm = ss|M
        xn = ss|N
        xm_count = scanD(xm, D)
        xn_count = scanD(xn, D)
        for api in api_list:
            xym = xm|api
            xyn = xn|api
            xym_count = scanD(xym, D)
            xyn_count = scanD(xyn, D)
            xy = ss|api


def myapriori(dataset, api_list):
    initset = map(set, [[api] for api in api_list])
    startset = initset
    for i in range(5):
        calcNext(startset, initset, dataset)
        i += 1



if __name__ == '__main__':
    dataset,api_list = loadData(10)
    myapriori(dataset, api_list)
