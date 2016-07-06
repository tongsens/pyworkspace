__author__ = 'Administrator'

import pymongo

class GetData():
    def __init__(self):
        pass

    def connect(self):
        db = pymongo.MongoClient(host='127.0.0.1', port=27017)
        hd = db.cuckoo.analysis
        return hd

    def filter_api(self, data):
        filename = data['target']['file']['name']
        proname = filename+'.exe'
        pid = 0
        for x in data['behavior']['processes']:
            if x['process_name'] == proname:
                pid = str(x['pid'])
                break
        if pid==0:
            ret_api= data['behavior']['apistats'].items()[0][1]
        else:
            ret_api = data['behavior']['apistats'][pid]
        return ret_api


    def printinfo(self, data):
        print 'md5:', data['target']['file']['md5']
        print 'filename:', data['target']['file']['name']
        print 'vrs:', data['virustotal']['positives']
        print 'api:', data['behavior']['apistats'].keys()
        prolist = [(x['pid'], x['process_name']) for x in data['behavior']['processes']]
        print 'process:', prolist
        print ''.center(80,'-')

    def getapidata(self, limit_num=100):
        db = self.connect()
        json_list = db.find({}, {'_id':0, 'target.file':1, 'virustotal.positives':1, 'behavior':1}).limit(limit_num)
        md5_list = []
        clss_list = []
        api_list = []
        for data in json_list:
            clss = data['virustotal']['positives']
            clss_list.append(clss)
            md5val = data['target']['file']['md5']
            md5_list.append(md5val)
            apis = self.filter_api(data)
            #self.printinfo(data)
            api_list.append(apis)
        return api_list, clss_list, md5_list

if __name__ == '__main__':
    gdata = GetData()
    api_list, clss_list, md5_list = gdata.getapidata(10)
    print api_list