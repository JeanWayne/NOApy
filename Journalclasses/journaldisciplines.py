import re
from nltk.corpus import stopwords
import re

from nltk.corpus import stopwords

stoplist = stopwords.words('english')
stoplist.append('etc.')


def capitalize(s):
	# tokens = s.split(' ')
	tokens = re.split(r'[, ]+', s)
	cap = []
	for t in tokens:
		if t not in stoplist:
			t = t[:1].upper() + t[1:]
		cap.append(t)
	return " ".join(cap)


def readjournalclasses(file):
	j2c = {}
	for line in file:
		fields = line.split(';')
		if len(fields) < 5:
			continue
		journal = fields[0].strip()
		area_raw = [s.strip() for s in re.split(r'\|', fields[3])]
		area = [capitalize(a) for a in area_raw]
		j2c[journal] = area
	return j2c


f = open('journalclassification.csv')
j2c = readjournalclasses(f)

# pprint.pprint(j2c)


from pymongo import MongoClient

client = MongoClient('mongodb://141.71.5.19:27017/')
# client = MongoClient('mongodb://localhost:27017/')

db = client.beta
# collection = db.Test20_9
# collection = db.hindawi_1505118371032
collection = db.Corpus

results = collection.find({})
for r in results:
	if 'journalName' in r:
		j = r['journalName']
		if j is None:
			continue
		j = j.strip()
		j = re.sub(r'\s+', ' ', j)
		if j not in j2c:
			print('Journal not found:', j)
		else:
			c = j2c[j]
			collection.update({'_id': r['_id']}, {'$unset': {'discipline': 1}}, multi=False)
			collection.update({'_id': r['_id']}, {'$set': {'discipline': c}}, upsert=False, multi=False)
