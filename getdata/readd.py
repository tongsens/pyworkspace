__author__ = 'Administrator'
import pymongo

class ReadData():
    def __init__(self):
        pass

    def connect(self, ip='127.0.0.1'):
        db = pymongo.MongoClient(host=ip, port=27017)
        handle = db.cuckoo.analysis
        return handle

    def findData(self, limit_num=10):
        db = self.connect('192.168.99.215')
        good_list = db.find({'virustotal.positives':0, 'target.file.md5':{'$exists':'true'}, 'behavior.apistats':{'$exists':'true'}}).limit(limit_num)
        bad_list = db.find({'virustotal.positives':{'$gt':20}, 'target.file.md5':{'$exists':'true'}, 'behavior.apistats':{'$exists':'true'}}).limit(limit_num)
        return good_list, bad_list

    def insertData(self, number=10):
        good_list,bad_list = self.findData(number)
        db = self.connect()
        num = 0
        for x in good_list:
            try:
                db.insert(x)
            except:
                pass
            try:
                db.insert(bad_list[num])
            except:
                pass
            num += 1

    def test(self):
        db = self.connect()
        json_list = db.find()
        for x in json_list:
            print x['virustotal']['positives']


if __name__ == '__main__':
    rd = ReadData()
    rd.insertData(5000)