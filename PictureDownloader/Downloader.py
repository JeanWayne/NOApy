import os

from pymongo import MongoClient
import urllib.request

client = MongoClient('141.71.5.19', 27017)
db = client['workshop']
collection = db['hindawi_1486555684003']
db_size= collection.find().count()
print(db_size)
cursor = collection.find()#{'DOI':'10.1155/2008/870804'})#[20:25]

for document in cursor:
	findings =document['findings']
	jN=document['journalName']
	jN=str(jN).strip()
	DOI=str(document['DOI'])
	DOI=DOI.replace("/","_")
	location=jN+"/"+DOI+"/"
	if not os.path.exists(jN):
		os.makedirs(jN)
	if not os.path.exists(jN+"/"+DOI):
		os.makedirs(jN+"/"+DOI)
	for find in findings:
		url = find['URL2Image']
		try:
			response = urllib.request.urlopen(url)
			data = response.read()  # a `bytes` object
		except urllib.error.HTTPError:
			print("Error at "+DOI)
			with open('Errors.txt', 'a', encoding="utf8") as m:
				m.write("Error@: "+DOI+"\n")
		#text = data.decode('utf-8')
		f = open(location+str(find['findingID'])+'.jpg', 'wb')
		f.write(data)
		f.close()
		with open(location+str(find['findingID'])+'.txt', 'a', encoding="utf8") as g:
			g.write(find['captionBody'])

		#print(find['URL2Image'])