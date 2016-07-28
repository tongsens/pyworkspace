__author__ = 'Administrator'

from getdata.getdata import *

def readFeature():
    import json
    with open('apilist.txt', 'r') as fp:
        buf = fp.read()
    api_list = json.loads(buf)
    return api_list

def loadData(num):
    gd = GetData()
    api_list, clss_list, md5_list = gd.getapidata(num)
    return api_list,clss_list

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            pass
            #print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def svmtray(feature ,clss):
    from sklearn import svm
    import numpy as np
    from sklearn import cross_validation
    X = np.array(feature)
    y = np.array(clss)
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2, random_state=0)
    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    print clf.score(X_test, y_test)

def clss_trans(clss_list):
    ret_list = []
    for i in clss_list:
        if i==0:
            ret_list.append(0)
        else:
            ret_list.append(1)
    return ret_list

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

if __name__ == '__main__':
    api_list, clss_list = loadData(3000)
    #feature = readFeature()
    feature = createVocabList(api_list)
    clss_list = clss_trans(clss_list)
    apiset = []
    for api in api_list:
        apiset.append(setOfWords2Vec(feature, api))
    svmtray(apiset, clss_list)