from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt
import numpy as np
import os
import os.path
from pymongo import MongoClient
import pymongo

rootpath="/home/noa/ImageDownloader"
### Helper methods
def giveLabel(s):
    if s[0][0]>=0.5:
        return "chart"
    else:
        return "nonChart"

# In[8]: Load Model

model=load_model("/home/noa/ImageDownloader/InceptionV3_0.06873_1000_4_1000_4.h5")
## Init Database connection
###############
client = MongoClient('141.71.5.19', 27017)
db = client['beta']
minlength = 1
collection = db['Corpus_Playground']
#collection = db['test']
#paper = collection.find({"numOfFindings":{"$gt":0}},no_cursor_timeout=True)
number = collection.find({"numOfFindings": {"$gt" : 0}, "findings.v1_chart_weights" :
    {"$exists": False}}, no_cursor_timeout=True).count()
paper = collection.find({"numOfFindings": {"$gt" : 0}, "findings.v1_chart_weights" :
    {"$exists": False}}, no_cursor_timeout=True)


num=0
print("Paper to Process: "+str(number))
for p in paper:
    path2file = p['path2file']
    publisher="noPublisher"
    if "Hindawi" in path2file:
        publisher = "Hindawi"
    elif "Springer" in path2file:
        publisher = "Springer"
    elif "PubMed" in path2file:
        publisher = "PubMed"
    journal=p['journalName']
    journalName = str(journal.replace(' ', '_'))

    year=p['year']
    DOI=p['DOI'].replace('/','_')
    num += 1
    print("Start Paper #"+str(num)+" of "+str(number))
    for f in p['findings']:
        findingID=f['findingID']
        # images/Hindawi/Advances_in_Acoustics_and_Vibration/2008/10.1155_2008_253948/3.jpg
        try:
            imgpath="images/"+str(publisher)+"/"+str(journalName)+"/"+str(year)+"/"+str(DOI)+"/"+str(findingID)+".jpg"
            completepath= rootpath+"/"+imgpath
            img = load_img(completepath, target_size=(224, 224))

            x = img_to_array(img)
            x.reshape((-1,) + x.shape)
            x = np.reshape(x, (-1, 224, 224, 3))
            s = model.predict(x)

            label=giveLabel(s)
            collection.update(
            {"_id": p['_id'], "findings.findingID": findingID},
            {
                "$set" : {"findings.$.v1_label":label}
            })

            collection.update(
            {"_id": p['_id'], "findings.findingID": findingID},
            {
                "$set" : {"findings.$.v1_chart_weights" : s[0].tolist()[0]}
            })
            collection.update(
            {"_id": p['_id'], "findings.findingID": findingID},
            {
                "$set" : {"findings.$.v1_nonChart_weight:" : s[0].tolist()[1]}
            })

        except:
            print("Error @ "+str(p['_id']))
            collection.update(
                {"_id": p['_id'], "findings.findingID": findingID},
                {
                    "$set": {"findings.$.DownloadError:": True}
                })


# Iterate over Images and give full path

# for dirpath, dirnames, filenames in os.walk("/home/EasyClass/schema"):
#     for filename in [f for f in filenames if f.endswith(".jpg")]:
#         complete= os.path.join(dirpath, filename)
#         path = os.path.normpath(dirpath)
#         path_split=path.split(os.sep)
#         print(path_split)
#         print(filename)
#



# #### TEST CLASSIFY:

#
# for root, dirs, files in os.walk("/home/EasyClass/schema"):
#     for file in files:
#         if file.endswith(".jpg"):
#              #print(os.path.join(root, file))
#             img = load_img(os.path.join(root, file), target_size=(224, 224))
#             #plt.imshow(img)
#             #plt.show()
#             x=img_to_array(img)
#             x.reshape((-1,) + x.shape)
#             x=np.reshape(x,(-1,224,224,3))
#             s=model.predict(x)
#             print(s)
#             print(giveLabel(s))
#

