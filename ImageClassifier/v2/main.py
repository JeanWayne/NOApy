# import ImageClassifier.v2.MongoHelper
from ImageClassifier.v2.MongoHelper import getUnclassifiedImages, updateImageWithLabel, getPathForImage, unsetLabels

unsetLabels()

# for i in getUnclassifiedImages(limit=10):
# 	print(getPathForImage(i['_id']))
# 	# classify
# 	updateImageWithLabel(i['_id'], "test2")
