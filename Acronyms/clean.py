from pymongo import MongoClient

client = MongoClient('mongodb://141.71.5.19:27017/')
db = client.beta
collection = db.Corpus_Playground

has_finding = collection.find({'numOfFindings': {'$gt': 0}})

for paper in has_finding:
	id = paper['_id']
	n = paper['numOfFindings']
	for i in range(n):
		collection.update({'_id': id}, {'$unset': {'findings.' + str(i) + '.abbreviation': 1}}, multi=True)
		collection.update({'_id': id}, {'$unset': {'findings.' + str(i) + '.acronym': 1}}, multi=True)
