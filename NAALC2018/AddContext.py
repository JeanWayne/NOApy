import re
from nltk.corpus import stopwords
import nltk
import json
import codecs
from pymongo import MongoClient

loc_for_abb='C:\Abbr\Abbreviations\examples.txt'
abb_norm_loc='C:\Abbr/abbreviations_normalized.json'
write_file_loc='C:\Abbr/'

def isAllowedToken(tested_string):
    """returns boolean if string contains allowed chars """
    match = re.match("^[A-Za-z0-9_-üöäÜÖÄß$&%§#~+.,]*$", tested_string)
    return match is not None
def checkTokenForPunctuation(string):
    """The name speaks itself"""
    if len(string)>1:
        if "." in string:
            return False
    return True

def toNOATokens(text):
    """Replace given String with a List of Tokens in NOA-Format
    """

    stop = set(stopwords.words('english'))
    #sentences=[]
    tokenList=[]
    s=text.lower()
    s=s.replace('-',' ')
    for t in nltk.word_tokenize(s):
        if isAllowedToken(t) and t not in stop and t not in (',') and len(t)>1:
            tokenList.append(t)
    return tokenList

txt = ""
with codecs.open(abb_norm_loc, 'r', 'utf-8') as data_file:
	for l in data_file:
		abbreviations = json.loads(l)


def replaceWithNormalizedCandidate(string):
	if string in abbreviations:
		return abbreviations[string]
	else:
		return string



def readData(csv):
	data = []
	for line in csv:
		columns = line.strip().split('\t')
		if len(columns) == 4:
			columns = list(map(lambda x: x.strip(), columns))
			data.append(columns)
	return data


csv = codecs.open(loc_for_abb, 'r', 'utf8')
data = readData(csv)
csv.close()

#################

client = MongoClient('141.71.5.19', 27017)
db = client['beta']
collection = db['Corpus_Playground']
#res=collection.find({"Exception":{"$exists": False}, "DOI":data[3][2]}, no_cursor_timeout=True)
#docs=[]
#################
#figure#
print(data[1])
print(toNOATokens(data[1][3]))
print(len(toNOATokens(data[1][3])))
lessThen=0

countDOIerror=0
print(len(data))
with open(write_file_loc+'ex_3_15_.context.txt', 'a',encoding="utf8") as the_file:
	for i in range(len(data)):
		content=""
		if data[i][2] is "":
			the_file.write(str(data[i][0]) + '\t' + str(data[i][1]) + '\t' + str(data[i][2]) + '\t' + str(data[i][3])+"\n")
			#countDOIerror=countDOIerror+1
			#print(data[i])
			continue


		res=collection.find({"Exception":{"$exists": False}, "DOI":data[i][2]}, no_cursor_timeout=True)
		print(str(i) + " \t\t DOI: " + data[i][2])
		for result in res:
			try:
				for finding in result['findings']:
					if data[i][0] in finding['captionBody']:
						for context in finding['context']:
							sent=nltk.sent_tokenize(context)
							for s in range(len(sent)):
								if "#figure#" in sent[s]:
									#print(str(len(toNOATokens(s)))+" len of example:"+str(len(toNOATokens(data[i][3]))))
									#the_file.write(data[0]+'\t'+data[1]+'\t'+data[2]+'\t'+data[3]+" "+s+"\n")
									if len(toNOATokens(content))<20:
										content=content+sent[s]+" "
										if s>0:
											content = content + sent[s-1] + " "
										if  len(sent)-s>1:
											content=content+sent[s+1]+" "
			except TypeError:
				1+1
		if len(toNOATokens(data[i][3]))>15:
			the_file.write(str(data[i][0]) + '\t' + str(data[i][1]) + '\t' + str(data[i][2]) + '\t' + str(data[i][3])+"\n")
		else:
			the_file.write(str(data[i][0]) + '\t' + str(data[i][1]) + '\t' + str(data[i][2]) + '\t' + str(data[i][3])+" "+content+"\n")
			lessThen += 1



#print(countDOIerror)
client.close()

#import numpy as np
#import matplotlib.pyplot as plt
#print(len(tp))
#plt.hist(binss, bins=1000)
#plt.title("Binss Histogram")
#plt.xlabel("Value")
#plt.ylabel("Frequency")
#plt.show()###


#plt.hist(addss, bins=100)
#plt.title("Adds Histogram")
#plt.xlabel("Value")
#plt.ylabel("Frequency")
#plt.show()