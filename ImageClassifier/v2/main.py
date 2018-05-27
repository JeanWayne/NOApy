# import ImageClassifier.v2.MongoHelper
from ImageClassifier.v2.MongoHelper import getUnclassifiedImages, updateImageWithLabel, getPathForImage, unsetLabels
from ImageClassifier.v2.PyTorchHelper import getImageClass

unsetLabels()

maxRun=10
iterLimit=10

for j in maxRun:
    for i in getUnclassifiedImages(limit=iterLimit):
        #print(getPathForImage(i['_id']))
        path=getPathForImage(i['_id'])
        label=getImageClass(path)
        updateImageWithLabel(i['_id'], "label")
    print("{0} Images Processed, starting next Query".format(iterLimit))
print("Completed {0} x {1} runs".format(maxRun,iterLimit))

