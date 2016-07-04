#连接数据库
pymongo.MongoClient(host=ip, port=27017)
#数据库条件查询{'$exists':'true'}
db.find({'virustotal.positives':0, 'target.file.md5':{'$exists':'true'}, 'behavior.apistats':{'$exists':'true'}})
#数据库查询返回cursor
json_list = db.find()