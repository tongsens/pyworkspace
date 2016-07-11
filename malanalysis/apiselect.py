__author__ = 'Administrator'

from getdata.getdata import *
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = inputSet[word]
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def drawpic(good_list, bad_list, api):
    drawlist = [good_list,bad_list]
    narr = np.array(drawlist).T
    df = pd.DataFrame(narr, columns=['normal', 'malware'])
    df.plot()
    plt.title(api)
    plt.show()

def countdata(data_list):
    data_count = [0,0,0,0,0]
    for x in data_list:
        if x>0:
            data_count[0] += 1
        if x>10:
            data_count[1] += 1
        if x>100:
            data_count[2] += 1
        if x>1000:
            data_count[3] += 1
        if x>5000:
            data_count[4] += 1
    return data_count


def drawbar(good_list, bad_list,api):
    good_count = countdata(good_list)
    bad_count = countdata(bad_list)
    drawlist = [good_count, bad_count]
    narr = np.array(drawlist).T
    df = pd.DataFrame(narr, index=[ '1+', '10+', '100+', '1000+', '5000+'], columns=['normal', 'malware'])
    df.plot(kind='bar')
    plt.title(api)
    plt.show()

class Tcount():
    def __init__(self, good_list, bad_list):
        self.badmax = self.getmax(bad_list)
        self.goodmax = self.getmax(good_list)
        self.badnzero = self.getnotzero(bad_list)
        self.goodnzero = self.getnotzero(good_list)
        self.badsum = self.getsum(bad_list)
        self.goodsum = self.getsum(good_list)
        self.grenum = self.grenum(bad_list, self.goodmax)
        #self.printdata()
        self.threod = self.calcthreod()

    def getthreod(self):
        return self.threod

    def printdata(self):
        print 'badmax:',self.badmax, 'goodmax:',self.goodmax
        print 'badnzero:',self.badnzero,'goodnzero:',self.goodnzero
        print 'greter number:',self.grenum,
        if (self.goodnzero>0) and (self.badnzero>0):
            print 'rate:',float(self.grenum)/float(self.goodnzero)
            print 'badsum:',float(self.badsum)/float(self.badnzero), 'goodsum:',float(self.goodsum)/float(self.goodnzero)

    def calcthreod(self):
        threod = 1
        if self.goodnzero==0:
            threod = int(self.badnzero)
            return threod
        elif self.badnzero==0:
            threod = float(0.0)
            return threod
        else:
            num1 = float(self.badmax - self.goodmax)/float(self.goodmax)
            #num2 = float(self.grenum)/float(self.goodnzero)
            num2 = float(self.grenum)
            t1 = float(self.badsum)/float(self.badnzero)
            t2 = float(self.goodsum)/float(self.goodnzero)
            num3 = (t1-t2)/t1
            threod = num1 * num2 * num3
            return threod

    def grenum(self, data, value):
        count = 0
        for x in data:
            if x>value:
                count += 1
        return count

    def getsum(self,data):
        return sum(data)

    def getmax(self, data):
        maxvalue = max(tuple(data))
        return maxvalue

    def getnotzero(self,data):
        count = 0
        for x in data:
            if x>0:
                count += 1
        return count

def apicount(vocablist, setlist, clss_list):
    ret_dict = {}
    for i,api in enumerate(vocablist):
        #print api
        bad_list = []
        good_list = []
        for j,clss in enumerate(clss_list):
            if clss==0:
                good_list.append(setlist[j][i])
            else:
                bad_list.append(setlist[j][i])
        #good_list.sort()
        #bad_list.sort()
        #print 'good_list:', good_list
        #print 'bad_list:', bad_list
        #print ''.center(80,'-')
        th = Tcount(good_list,bad_list)
        ret_dict[api] = th.getthreod()
        #drawpic(good_list, bad_list, api)
        #drawbar(good_list, bad_list, api)
        #os.system("pause")
    un_feature = []
    good_feature = []
    bad_feature = []
    for data in ret_dict.items():
        if isinstance(data[1], int):
            un_feature.append(data)
        elif data[1]>3.0:
            good_feature.append(data)
        else:
            bad_feature.append(data)
    un_feature.sort(key=lambda f:f[1])
    good_feature.sort(key=lambda f:f[1])
    bad_feature.sort(key=lambda f:f[1])
    print un_feature
    print good_feature
    print bad_feature


def selectModel(vocablist,setlist, clss_list):
    from sklearn.svm import LinearSVC
    from sklearn.feature_selection import SelectFromModel
    X = np.array(setlist)
    y = np.array(clss_list)
    svc = LinearSVC(C=0.01, penalty='l1', dual=False)
    lsvc = svc.fit(X,y)
    model = SelectFromModel(lsvc, prefit=True)
    X_new,mask = model.transform(X)
    good_feature = []
    bad_feature = []
    for idx in range(mask.shape[0]):
        if mask[idx]:
            good_feature.append(vocablist[idx])
        else:
            bad_feature.append(vocablist[idx])
    print X.shape
    print X_new.shape
    print good_feature
    print bad_feature

def treebaseSelect(vocablist, setlist, clss_list):
    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.feature_selection import SelectFromModel
    X = np.array(setlist)
    y = np.array(clss_list)
    clf = ExtraTreesClassifier()
    clf = clf.fit(X,y)
    model = SelectFromModel(clf, prefit=True)
    X_new, mask = model.transform(X)
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
    gd = GetData()
    api_list,clss_list,md5_list = gd.getapidata(3000)
    vocablist =  createVocabList(api_list)
    setlist = []
    for x in api_list:
        setlist.append(setOfWords2Vec(vocablist, x))
    apicount(vocablist, setlist, clss_list)
