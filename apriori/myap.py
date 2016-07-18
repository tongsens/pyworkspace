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

######################################################

def calcValue(xm, xn, ym, yn, xym, xyn):
    x = float(xm)/float(xm+xn)
    y = float(ym)/float(ym+yn)
    xy = float(xym)/float(xym+xyn)
    maxvale = max(x,y)
    threod = (xy-maxvale)*xym
    return threod,(xy-maxvale),xy,x,y

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
            ym = api|M
            yn = api|N
            ym_count = scanD(ym, D)
            yn_count = scanD(yn, D)
            xym_count = scanD(xym, D)
            xyn_count = scanD(xyn, D)
            xy = ss|api
            xy_count = scanD(xy, D)
            if xy_count>0:
                oth = calcValue(xm_count,xn_count,ym_count, yn_count, xym_count,xyn_count)
                if oth[0]>2.0 and oth[1]>0.1 and oth[2]>0.9:
                    print xy,oth, xym_count
        #os.system("pause")


def myapriori(dataset, api_list):
    initset = map(set, [[api] for api in api_list])
    startset = initset
    for i in range(5):
        calcNext(startset, initset, dataset)
        i += 1

##############################################

def genL(apilist, dataset):
    M = set([u'malware'])
    N = set([u'normal'])
    key_list = []
    for api1 in apilist:
        for api2 in apilist:
            key_list.append(api1|api2)
    key_dict = map(frozenset, key_list)
    result_dict = {}
    mal_dict = {}
    print 'running...'
    for key in key_dict:
        subseq = set(key)
        xm = subseq|M
        xn = subseq|N
        xm_count = scanD(xm, dataset)
        xn_count = scanD(xn, dataset)
        if (xm_count+xn_count)>0:
            rate = float(xm_count)/float(xm_count+xn_count)
        else:
            rate = 0
        mal_dict[frozenset(xm)] = xm_count
        result_dict[key] = rate
    return result_dict, mal_dict

def calcData(count_dict, dataset, mal_dict):
    M = set([u'malware'])
    for data in count_dict.items():
        key = list(data[0])
        if data[1] > 0.9 and len(key)==2:
            x_rate = count_dict[frozenset([key[0]])]
            y_rate = count_dict[frozenset([key[1]])]
            maxvalue = max(x_rate, y_rate)
            grow = data[1]-maxvalue
            mals_num = mal_dict[frozenset(set(data[0])|M)]
            if grow>0.1 and mals_num>10:
                print key, (x_rate, y_rate, grow, data[1], mals_num)

def apriori(dataset, apilist):
    initset = map(set, [[api] for api in api_list])
    count_dict,mal_dict = genL(initset, dataset)
    calcData(count_dict, dataset, mal_dict)


if __name__ == '__main__':
    dataset,api_list = loadData(3000)
    apriori(dataset, api_list)
