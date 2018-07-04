import os
import urllib
from pymongo import MongoClient
from urllib import request

current = 0
client = MongoClient('141.71.5.22', 27017)
dbn = client['NewSchema']
##### Read Collection
collection = dbn['Corpus_Image_1526627740266']
size = collection.find().count()
print(f"Images in this Collection: {size}")
##########
findings = collection.find({}, no_cursor_timeout=True)
with open(".txt", "w") as text_file:
	for f in findings:
		# s contains the string with the URL to a Image
		s = f["URL2Image"]
		print(s)

		# this comment writes the string to a file
		# print(f"{s}\n", file=text_file)

		# coment out this break to process all data
		break
findings.close()
