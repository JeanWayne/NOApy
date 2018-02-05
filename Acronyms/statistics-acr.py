# coding: utf-8

# # Some statistics about abreviations

# In[ ]:

import pprint

from pymongo import MongoClient

client = MongoClient('mongodb://141.71.5.19:27017/')

db = client.beta
collection = db.Corpus_Playground
findings = collection.find({'numOfFindings': {'$gt': 0}})

dictionary = {}

for f in findings:
	flist = f['findings']
	journal = f['journalName']
	for img in flist:
		if 'abbreviation' in img:
			for abrexp in img['abbreviation']:
				abr = abrexp[0]
				exp = abrexp[1]
				if exp == None:
					continue
				exps = dictionary.get(abr, [])
				if exp not in exps:
					exps.append(exp)
					dictionary[abr] = exps

print("Number of abbreviations: ", len(dictionary))
unamb = 0
nrOfExps = 0
found = 0
for abr in dictionary:
	n = len(dictionary[abr])
	if n == 1:
		unamb += 1
	if n > 0:
		found += 1
	nrOfExps += n

print("Number of resolved abbreviations: ", found)
print("Number of unambiguous abbreviations: ", unamb)
print("Average number of definitions: ", float(nrOfExps) / float(len(dictionary)))
pprint.pprint(dictionary)
