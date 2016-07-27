__author__ = 'Administrator'

from getdata.getdata import *
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import pymongo

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def load_data(num=100, type=1):
    gd = GetData()
    api_list,clss_list,md5_list = gd.getapidata(num)
    vblist = createVocabList(api_list)
    good_list = []
    bad_list = []
    good_dict = []
    bad_dict = []
    for i,data in enumerate(api_list):
        if clss_list[i]>0:
            bad_list.append(data.keys())
            bad_dict.append(data)
        else:
            good_list.append(data.keys())
            good_dict.append(data)
    if type==1:
        return good_list,bad_list,vblist
    else:
        return good_dict,bad_dict,vblist

def good_turning(data_list, threod):
    record_list = [0]*threod
    for i in range(threod):
        for data in data_list.items():
            if data[1] == i:
                record_list[i] += 1
    turning_list = []
    print record_list
    for r in range(threod-1):
        dr = float((r+1)*record_list[r+1])/float(record_list[r])
        turning_list.append(dr)
    ret_dict = {}
    for data in data_list.items():
        if data[1]<threod-1:
            ret_dict[data[0]] = turning_list[data[1]]
        else:
            ret_dict[data[0]] = data[1]
    return ret_dict

def api_count(good_list,bad_list,vblist):
    good_count ={}
    bad_count = {}
    for api in vblist:
        good_count[api] = 0
        for gapi in good_list:
            if api in gapi:
                good_count[api] += 1
        bad_count[api] = 0
        for bapi in bad_list:
            if api in bapi:
                bad_count[api] += 1
    good_new_list = good_turning(good_count, 5)
    bad_new_list = good_turning(bad_count, 5)
    return good_new_list,bad_new_list

def api_time(good_list,bad_list, vblist):
    good_count ={}
    bad_count = {}
    for api in vblist:
        good_count[api] = 0
        for gapi in good_list:
            if api in gapi.keys():
                good_count[api] += gapi[api]


def count_rate(g_list, b_list, vblist):
    ret_dict = {}
    ret_list = []
    for api in vblist:
        rate = float(b_list[api])/float(g_list[api]+b_list[api])
        ret_dict[api] = rate
        ret_list.append((api, rate))
    ret_list.sort(key=lambda f:f[1], reverse=True)
    return ret_dict

def getP(data_dict):
    datalist = [item[1] for item in data_dict.items()]
    total = sum(datalist)
    ret_dict = {}
    for key in data_dict:
        ret_dict[key] = float(data_dict[key])/float(total)
    return ret_dict


def twoArgCount(datalist,vblist):
    combie_list = []
    for ap1 in vblist:
        for ap2 in vblist:
            tmp = set([ap1, ap2])
            if len(tmp)==2 and tmp not in combie_list:
                combie_list.append(tmp)
    key_list = map(frozenset, combie_list)
    dataset = map(set, datalist)
    ret_dict = {}
    for key in key_list:
        ret_dict[key] = 0
        for data in dataset:
            if key.issubset(data):
                ret_dict[key] += 1
    new_dict = good_turning(ret_dict,6)
    return new_dict

def entroy(pdict):
    import math
    entlist = [-item[1]*math.log(item[1], 2) for item in pdict.items()]
    return sum(entlist)

def combieEntroy(twodict, onedict):
    import math
    ret_dict = {}
    for data in twodict.items():
        key = data[0]
        pxy = data[1]
        x_key = list(key)[0]
        y_key = list(key)[1]
        px = onedict[x_key]
        py = onedict[y_key]
        cmbxy = math.log(pxy/(px*py),2)
        ret_dict[key] = cmbxy
    return ret_dict

def analysis(bad_combie, twobad, twogood, rate_dict):
    res_list = []
    for key in twobad:
        k1 = list(key)[0]
        k2 = list(key)[1]
        px = rate_dict[k1]
        py = rate_dict[k2]
        rate = twobad[key]/(twobad[key]+twogood[key])
        upvalue = rate - max(px,py)
        res_list.append((key, rate, bad_combie[key], px, py, upvalue))
    res_list.sort(key=lambda f:f[2], reverse=True)
    for data in res_list:
        if data[1]>0.9 and data[5]>0.05:
            print data


def run_rate():
    good_list,bad_list,vblist = load_data(3000, type=1)
    g_list, b_list = api_count(good_list,bad_list,vblist)
    goodP = getP(g_list)
    badP= getP(b_list)
    ret_g = entroy(goodP)
    ret_b = entroy(badP)

    twogood = twoArgCount(good_list,vblist)
    twobad = twoArgCount(bad_list, vblist)
    tgP = getP(twogood)
    tbP = getP(twobad)

    bad_combie = combieEntroy(tbP, badP)
    good_combie = combieEntroy(tgP, goodP)


    rate_dict = count_rate(g_list, b_list, vblist)
    analysis(bad_combie, twobad, twogood, rate_dict)

if __name__ == '__main__':
    run_rate()
