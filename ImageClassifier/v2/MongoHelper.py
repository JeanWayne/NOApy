from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('141.71.5.22', 27017)
# db = client['beta']
db = client['NewSchema']

minlength = 1
ImagesC = db['Corpus_Image_1525787622302']
JournalC = db['Corpus_Journal_1525787622302']

number = ImagesC.find({"image_class": {"$exists": False}}).count()
print(number)
numbertw = JournalC.find({"image_class": {"$exists": False}}).count()
print(numbertw)


def getPathForImage(DBObjectName):
	o = ObjectId(DBObjectName)
	ret = JournalC.find({"findingsRef": o})
	# ret=JournalC.find({"numOfFindings":4}).limit(1)
	img = ImagesC.find({"_id": o})
	findingID = -1
	for i in img:
		findingID = i['findingID']
	for r in ret:
		try:
			path2file = r['path2file']
			publisher = "noPublisher"
			if "Hindawi" in path2file:
				publisher = "Hindawi"
			elif "Springer" in path2file:
				publisher = "Springer"
			elif "PubMed" in path2file:
				publisher = "PubMed"
			elif "Copernicus" in path2file:
				publisher = "Copernicus"
			elif "newFrontiers" in path2file:
				publisher = "newFrontiers"
			journal = r['journalName']
			journalName = str(journal.replace(' ', '_'))
			year = r['year']
			DOI = r['DOI'].replace('/', '_')
			imgpath = "/home/noa/noaImages/" + str(publisher) + "/" + str(journalName) + "/" + str(year) + "/" + str(
				DOI) + "/" + str(findingID) + ".jpg"
			return imgpath

		except:
			print("Error @ " + str(o))
			# collection.update(
			#     {"_id": p['_id'], "findings.findingID": findingID},
			#     {
			#         "$set": {"findings.$.DownloadError:": True}
			#     })
			return "ERROR"


def updateImageWithLabel(DBObjectName, label):
	o = ObjectId(DBObjectName)
	ImagesC.update({"_id": o}, {"$set": {"image_class": label}})


def getUnclassifiedImages(limit=100):
	return ImagesC.find({"image_class": {"$exists": False}}).limit(limit)


print(getPathForImage("5af1abe7e106db27a4447248"))
