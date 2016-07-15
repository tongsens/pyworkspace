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

def datachange(api_list):
    ret_list = []
    for api in api_list.items():
        apiname = api[0]
        if(api[1])==0:
            apiname += '0'
        if(api[1])>0 and (api[1])<=10:
            apiname += '1'
        if(api[1])>10 and (api[1])<=100:
            apiname += '10'
        if(api[1])>100:
            apiname += '100'
        ret_list.append(apiname)
    return ret_list

def load_data(num=100):
    gd = GetData()
    api_list,clss_list,md5_list = gd.getapidata(num)
    new_api_list = []
    for data in api_list:
        new_api_list.append(datachange(data))
    vocablist =  createVocabList(new_api_list)
    setlist = []
    for x in new_api_list:
        setlist.append(setOfWords2Vec(vocablist, x))
    return vocablist, setlist, clss_list

def bayers(vocablist, setlist, clss_list):
    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.feature_selection import SelectFromModel
    X = np.array(setlist)
    Y = np.array(clss_list)
    clf = ExtraTreesClassifier()
    clf = clf.fit(X,Y)
    model = SelectFromModel(clf, prefit=True)
    X_new,mask = model.transform(X)
    good_feature = []
    bad_feature = []
    for idx in range(mask.shape[0]):
        if mask[idx]:
            good_feature.append(vocablist[idx])
        else:
            bad_feature.append(vocablist[idx])
    print good_feature
    print bad_feature



if __name__ == '__main__':
    #vocablist, setlist, clss_list = load_data(1000)
    #bayers(vocablist,setlist,clss_list)
    db = pymongo.MongoClient(host='127.0.0.1', port=27017)
    xx = db.cuckoo.analysis
    print xx.count()