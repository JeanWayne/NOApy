import time

from nltk.tokenize import WhitespaceTokenizer
from pymongo import MongoClient

tokenizer = WhitespaceTokenizer()
import json

## John's local host section
# client = MongoClient()
# db = client.NLP
# collection = db.wiki

## Christian's server section
client = MongoClient('mongodb://141.71.5.19:27017/')
db = client.beta
collection = db.Corpus_Playground

total_time = time.time()
start = time.time()

##########################################################################################
#           build the cluster dictionary
##########################################################################################
print('Stage 1')
with open("abbreviations_clust.json") as data_file:
	abrclust = json.loads(data_file.read())
normalform = {}
for abr in abrclust:
	for cluster in abrclust[abr]:
		if not isinstance(cluster, str):
			for definition in cluster[1:]:
				if definition in normalform:
					print('conflict: ' + definition + ' ' + cluster[0] + ' ' + normalform[definition])
				normalform[definition] = cluster[0]
				# print(definition + ' --> '  +  cluster[0])

##########################################################################################
#           build the dictionary from the query
##########################################################################################
print('Stage 2')

# only grab instances where an abrev is found
has_abbreviation = collection.find({'findings.acronym': {'$exists': 'true'}})

# journal name is its key
dict_of_journals = {}

for paper in has_abbreviation:
	journalabbr = dict_of_journals.get(paper['journalName'], {})
	for finding in paper['findings']:
		if 'acronym' in finding:
			for abbreviation in finding['acronym']:
				acro = abbreviation[0]
				definition = abbreviation[1]
				if definition == None:
					continue
				# print(acro,definition)
				if definition in normalform:
					definition = normalform[definition]
				defs = journalabbr.get(acro, [])
				if definition not in defs:
					defs.append(definition)
				journalabbr[acro] = defs
	dict_of_journals[paper['journalName']] = journalabbr

#####################################################
# updating mongodb with all results
#####################################################
print('Stage 3')

has_abbreviation = collection.find({'findings.acronym': {'$exists': 'true'}})
updates = 0
for paper in has_abbreviation:
	paperID = paper['_id']
	for finding in paper['findings']:
		if 'acronym' in finding:
			i = 0
			for abbreviation in finding['acronym']:
				acro = abbreviation[0]
				definition = abbreviation[1]
				if definition == None and acro in dict_of_journals[paper['journalName']]:
					journaldef = dict_of_journals[paper['journalName']][acro]
					if len(journaldef) == 1:
						findingID = finding['findingID']
						updates += 1
						# print(paper['DOI'],findingID,acro,journaldef[0])
						collection.update({'_id': paperID}, {
							'$set': {'findings.' + str(findingID) + '.acronym.' + str(i): (acro, journaldef[0])}},
						                  upsert=False, multi=False)
			i += 1

print("Definitions found: ", updates)
print("total time (with mongodb update):", time.time() - total_time)
