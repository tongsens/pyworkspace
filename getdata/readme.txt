#�������ݿ�
pymongo.MongoClient(host=ip, port=27017)
#���ݿ�������ѯ{'$exists':'true'}
db.find({'virustotal.positives':0, 'target.file.md5':{'$exists':'true'}, 'behavior.apistats':{'$exists':'true'}})
#���ݿ��ѯ����cursor
json_list = db.find()