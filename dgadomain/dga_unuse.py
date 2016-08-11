__author__ = 'Administrator'

import pymongo

def readUrl():
    db = pymongo.MongoClient(host='192.168.99.215', port=27017)
    hd = db.cuckoo.analysis
    json_list = hd.find({'network.domains':{'$exists':True}}, {'_id':0, 'network.domains':1})
    urlset = set()
    for data in json_list:
        for x in data['network']['domains']:
            url = x['domain']
            urlset.add(url)
    tocsv(urlset)

def tocsv(data):
    data_list = []
    for i,x in enumerate(data):
        data_list.append((i,x))
    import csv
    csvfile = file('url.csv','wb')
    writer = csv.writer(csvfile)
    writer.writerows(data_list)
    csvfile.close()

if __name__ == '__main__':
    readUrl()