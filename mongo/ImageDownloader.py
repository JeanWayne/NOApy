import urllib

from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib import request
import re
import os


current = 0
client = MongoClient('insert_IP', 27017)
db = client['NewSchema']
##### Read Collection
imageCollection = db['AllImages']
journalCollection = db['AllArticles']
#size = imageCollection.find({"URL2Image": {"/.*Springer.*/"}}).count()
imagecount = 0
i_skipped = 0
######
download = False
write2File = True
write2Collection = False
target_col = db['Images_21_11_2017']
##########
regx1 = re.compile("/.*springer.*/")

findings = imageCollection.find({"URL2Image": regx1, "image_class":"ERROR_IO"})


for f in findings:
	DOI = f['originDOI']
	source = f['source_id']
	URL = f['URL2Image']
	findingID = f['findingID']
	CAPTION = f['captionBody']

	article = journalCollection.find_one({"_id": ObjectId(source)})
	journalName = str(article['journalName'])
	pathJournalName = str(article['journalName']).replace(' ', '_')
	year = article['year']
	Dumb_DOI = str(DOI).replace('/', '_')
	path2file = article['path2file']
	publisher= ""
	publisher = str(article['publisher'])
	if "Hindawi" in path2file:
		publisher = "Hindawi"
	elif "Springer" in path2file:
		publisher = "Springer"
	elif "PubMed" in path2file:
		publisher = "PubMed"
	elif "PMC" in path2file:
		publisher = "PubMed"
	elif "Copernicus" in publisher:
		publisher = "Copernicus"
	elif "frontiers" in path2file:
		publisher = "Frontiers"
	path = str(publisher) + '/' + str(pathJournalName) + '/' + str(year) + '/' + str(Dumb_DOI) + '/'
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
		with open("D:\Image_Files_URLS_betaCorpus_v7.txt", 'a', encoding="utf-8") as myfile:
			print(path)
			print(URL)
			myfile.write(URL + " " + root + path + str(findingID) + ".jpg" + "\n")
	elif write2Collection:
		DOI = str(Dumb_DOI).replace('_', '/')

		document = {"journalName": journalName,
					"year": year,
					"DOI": DOI,
					"title": article['title'],
					"authors": article['authors'],
					"URL": f['URL2Image'],
					"TIB_URL": root + path + str(findingID) + ".jpg",
					"CaptionBody": f['captionBody'],
					"CaptionTitle": f['captionTitle'],
					"Context": f["context"],
					"CopyrightFlag": f['Copyrightflag'],
					"License": f["license"],
					"LicenseType": f["LicenseType"]
					}
		print(DOI)
		if 'v1_label' in f:
			label=str(f['v1_label'])
			if label=="chart":
				document['ImageType']="chart"
			elif label=="nonChart":
				document['ImageType']="image"
		if 'acronym' in f:
			arr=[]
			for acc in f['acronym']:
				arr.append(acc[1])
			document["Expanded"] = arr
		if 'discipline' in f:
			document["discipline"] = f['discipline']
		if 'DownloadError:' not in f:
			target_col.insert_one(document)
		else:
			i_skipped+=1
			print("Error skipped #"+str(i_skipped))
print("end")
print(imagecount)
print("Image URLs found")
