import urllib

from pymongo import MongoClient
from urllib import request
import os


current = 0
client = MongoClient('141.71.5.19', 27017)
db = client['beta']
##### Read Collection
collection = db['Corpus_Playground']
size = collection.find().count()
imagecount = 0
i_skipped = 0
######
download = False
write2File = False
write2Collection = True
target_col = db['Images_29_1_2018']
##########
findings = collection.find({"numOfFindings": {"$gt": 0}}, no_cursor_timeout=True)
for f in findings:
	journalName = str(f['journalName'])
	pathJournalName = str(f['journalName']).replace(' ', '_')
	year = f['year']
	DOI = f['DOI']
	Dumb_DOI = str(DOI).replace('/', '_')
	for j in f['findings']:
		URL = j['URL2Image']
		findingID = j['findingID']
		path2file = f['path2file']
		CAPTION = j['captionBody']
		publisher= ""
		publisher = str(f['publisher'])
		if "Hindawi" in path2file:
			publisher = "Hindawi"
		elif "Springer" in path2file:
			publisher = "Springer"
		elif "PubMed" in path2file:
			publisher = "PubMed"
		elif "Copernicus" in publisher:
			publisher = "Copernicus"
		path = publisher + '/' + pathJournalName + '/' + year + '/' + Dumb_DOI + '/'
		root = "images/"
		path2 = root + path
		imagecount += 1
		if download:
			if not os.path.exists(path2):
				os.makedirs(path2)
			print(URL)
			try:
				img = open(root + path + str(findingID) + ".jpg", 'wb')
				img.write(request.urlopen(URL).read())
				img.close()
			except urllib.error.HTTPError:
				with open(root + "Error.txt", 'a') as err:
					err.write(str(DOI) + "  -> got an Error!\n")
				print("ERROR")
			with open(root + path + str(findingID) + ".txt", 'a', encoding="utf-8") as myfile:
				myfile.write("DOI: " + str(DOI) + "\n")
				myfile.write("IMGURL: " + str(URL) + "\n")
				myfile.write("Caption: " + str(CAPTION))
			print("wrote #" + str(current))
			current += 1
		elif write2File:
			with open("C:\Image_Files_URLS_betaCorpus_v3.txt", 'a', encoding="utf-8") as myfile:
				print(path)
				print(URL)
				myfile.write(URL + " " + root + path + str(findingID) + ".jpg" + "\n")
		elif write2Collection:
			DOI = str(Dumb_DOI).replace('_', '/')

			document = {"journalName": journalName,
			            "publisher": f['publisher'],
			            "year": year,
			            "DOI": DOI,
			            "title": f['title'],
			            "authors": f['authors'],
			            "URL": j['URL2Image'],
			            "TIB_URL": root + path + str(findingID) + ".jpg",
			            "CaptionBody": j['captionBody'],
			            "CaptionTitle": j['captionTitle']
			            }
			if 'v1_label' in j:
				label=str(j['v1_label'])
				if label=="chart":
					document['ImageType']="chart"
				elif label=="nonChart":
					document['ImageType']="picture"
			if 'acronym' in j:
				arr=[]
				for acc in j['acronym']:
					arr.append(acc[1])
				document["Expanded"] = arr
			if 'discipline' in f:
				document["discipline"] = f['discipline']
			if 'DownloadError:' not in j:
				target_col.insert_one(document)
			else:
				i_skipped+=1
				print("Error skipped #"+str(i_skipped))
print("end")
print(imagecount)
print("Image URLs found")

