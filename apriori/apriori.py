__author__ = 'Administrator'

from getdata.getdata import *
import os

def loadDataSet():
    return [[1,3,4], [2,3,5], [1,2,3,5], [2,5]]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can):
                    ssCnt[can] =  1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList

def apriori(dataSet, minSupport = 0.4):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    count = 0
    while (len(L[k-2]) > 0):
        print count
        if count>0:
            break
        Ck = aprioriGen(L[k-2], k)
        Lk , supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k+= 1
        count += 1
    return L,supportData

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
    return ret_list

def dataPrint(supportData, idx):
    outlen = []
    for data in supportData.items():
        if len(data[0])==idx:
            outlen.append(data)
    outlen.sort(key=lambda f:f[1],reverse=True)
    for data in outlen:
        if u'malware' in data[0] or 'normal' in data[0]:
            print data

def findSubSeq(data,supData, keyname):
    seq = []
    for key in data[0]:
        if key!=keyname:
            seq.append([key])
    fset = map(frozenset, seq)
    if len(fset)>0:
        return supData[fset[0]]
    return 1

def calcConf(supData, keyname):
    conf_list = []
    for data in supData.items():
        if keyname in data[0]:
            conf = data[1]/findSubSeq(data, supData, keyname)
            conf_list.append((data,conf))
    conf_list.sort(key=lambda f:f[1], reverse=True)
    for data in conf_list:
        print data

if __name__ == '__main__':
    dataset = loadData(3000)
    L, supportData = apriori(dataset, 0.01)
    calcConf(supportData, u'normal')