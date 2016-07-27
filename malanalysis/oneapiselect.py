#coding:utf-8
__author__ = 'Administrator'
'''
select one api that may used by malware
add good-turning fix div zero error
'''

from getdata.getdata import *

def loadData(num):
    gd = GetData()
    api_list,clss_list,md5_list = gd.getapidata(num)
    return api_list,clss_list

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

class dataCount():
    def __init__(self, data, clss):
        self.data = data
        self.clss = clss
        self.apilist = createVocabList(self.data)
        self.good_time_count, self.bad_time_count = self.callTimesCount(self.data, self.clss,1)
        self.good_has_count, self.bad_has_count = self.callTimesCount(self.data, self.clss,2)

    #统计调用次数，和是否包含。 type=2 是为是否包含
    def callTimesCount(self, data, clss, type):
        good_count = {}
        bad_count = {}
        for api in self.apilist:
            good_count[api] = 0
            bad_count[api] = 0
        for i,subdata in enumerate(data):
            if clss[i]==0:
                for api in subdata:
                    if type==2:
                        good_count[api] += 1
                    else:
                        good_count[api] += subdata[api]
            else:
                for api in subdata:
                    if type==2:
                        bad_count[api] += 1
                    else:
                        bad_count[api] += subdata[api]
        return self.good_turning(good_count,6), self.good_turning(bad_count, 6)

    #用古德图灵方法平滑处理
    def good_turning(self, data_dict, k):
        time_list = [0]*k
        for data in data_dict.items():
            for i in range(k):
                if data[1] == i:
                    time_list[i] += 1
        fix_list = [0]*(k-1)
        for i in range(k-1):
            fix_list[i] = float(i+1)*time_list[i+1]/float(time_list[i])
        for key in data_dict:
            value = data_dict[key]
            if value<k-1:
                data_dict[key] = fix_list[value]
        return data_dict

    #返回最后的统计数据
    def getCountData(self):
        return self.good_time_count, self.bad_time_count, self.good_has_count,self.bad_has_count

class analysisApi():
    def __init__(self, countdata):
        self.gtc, self.btc, self.ghc, self.bhc = countdata
        self.timerate = self.calcRate(self.gtc, self.btc)
        self.hasrate = self.calcRate(self.ghc, self.bhc)

    def calcRate(self, good_count, bad_count):
        rate = {}
        for key in good_count:
            rate[key] = float(bad_count[key])/float(good_count[key] + bad_count[key])
        return rate

    def sub(self, a, b):
        return a-b

    def mul(self, a, b):
        return a*b

    #计算贡献值
    def calcPP(self, type='mul'):
        out_list = []
        if type=='sub':
            func = self.sub
        else:
            func = self.mul
        for key in self.timerate:
            out_list.append((key,func(self.timerate[key], self.hasrate[key])))
        out_list.sort(key=lambda f:f[1], reverse=True)
        for x in out_list:
            print x


if __name__ == '__main__':
    api_list, clss_list = loadData(3000)
    dcount = dataCount(api_list, clss_list)
    countdata = dcount.getCountData()
    alysapi = analysisApi(countdata)
    alysapi.calcPP(type='mal')
