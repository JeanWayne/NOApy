# coding: utf-8

# In[1]:

import codecs
import json

data_file = codecs.open('abbreviations_clust.json', 'r', 'utf-8')
abbreviations = json.loads(data_file.read())
data_file.close()


# In[2]:

def tgram(string):
	liste = []
	if 3 < len(string):
		for p in range(len(string) - 2):
			tg = string[p:p + 3]
			liste.append(tg)
	return liste


def tgo(s, t):
	stg = tgram(s)
	ttg = tgram(t)
	schnitt = 0
	for a in stg:
		if a in ttg:
			schnitt += 1
	vereinigung = len(stg) + len(ttg) - schnitt
	return float(schnitt) / float(vereinigung)


def alldifferent(clusters):
	for c in clusters:
		for c1 in clusters:
			if c[0] == c1[0]:
				continue
			if tgo(c[0], c1[0]) > 0.4:
				return False
	return True


def filternice(abbr):
	selection = {a: e for (a, e) in abbr.items() if 1 < len(e) < 6 and alldifferent(e)}  # tgo(e[0][0],e[1][0]) < 0.4}

	return selection


# In[3]:

filtered = filternice(abbreviations)
print(len(filtered))

# In[6]:

import pprint

pprint.pprint(filtered)

# Basically John's Code for finding definitions.

# In[4]:

# import time
from nltk.tokenize import sent_tokenize, WhitespaceTokenizer
import re
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()
from nltk import word_tokenize
from pymongo import MongoClient

tokenizer = WhitespaceTokenizer()
client = MongoClient('mongodb://141.71.5.19:27017/')
db = client.beta
collection = db.Corpus_Playground

print("connected")


def find_acronym_definitions(acronym, sent_list):
	for words_list in sent_list:  # CW 20171009
		if (acronym in words_list):
			for j in range(len(words_list)):
				if acronym == words_list[j] and '(' in words_list[(j - 1)] and ')' in words_list[j + 1]:
					boo = True
					acr_len = len(acronym)
					for k in range(acr_len):
						# minus one to get over the parenthesis
						if acronym[k] != words_list[j + k - acr_len - 1][0].upper():
							boo = False
							break
					if boo:
						out = ' '.join(str(x) for x in (words_list[j - k - 2:j - 1]))
						incluster = False
						if acronym in filtered:
							clusters = filtered[acronym]
							for clust in clusters:
								if out in clust:
									out = clust[0]
									incluster = True
									break
						if incluster:
							return (out)
	return (None)


def clean_paper_body(body1):
	# change a hypenated word into two words
	body2 = re.sub('-|\n|\t', ' ', body1)
	# remove all periods.  Current coding scheme wouldn't catch arconyms such as "G.R.B", so if we remove periods
	# we can catch it as "GRB"
	cleaned = re.sub('\.', '', body2)
	return cleaned


# ## find all acronyms and definitions

# In[7]:

def wordoverlap(a, b):
	toka = a.split(" ")
	tokb = b.split(" ")
	schnitt = 0
	for t in toka:
		if t in tokb:
			schnitt += 1
	vereinigung = len(toka) + len(tokb) - schnitt
	return float(schnitt) / float(vereinigung)


def newexample(ex, exlist):
	if ex in exlist:
		return False
	for e in exlist:
		if (wordoverlap(e, ex) > 0.5):
			return False
	return True


def find_examples():
	examples = {}
	for paper in collection.find({'numOfFindings': {'$gt': 0}}):
		if 'body' not in paper or not isinstance(paper['body'], str):
			continue
		full_acr_list = []
		# list of finding indexes
		findings_list = []
		# goes through each image caption
		for i in range(len(paper['findings'])):
			cleaned_body = ""
			if (paper['findings'][i]['captionBody'] != None):
				# clean all but alphanumeric letters, periods and dashes
				cleaned_body = re.sub('[^A-Za-z.-]', ' ', paper['findings'][i]['captionBody'])
			tok_body = tokenizer.tokenize(cleaned_body)
			for acr in tok_body:
				# remove periods, and leading/tailing dashes
				cleaned_acronym = re.sub('\-|\.|-$', '', acr)
				if cleaned_acronym.isupper() and len(cleaned_acronym) > 2:
					acronyms_list = [item[0] for item in full_acr_list]
					findings_list = [item[1] for item in full_acr_list]
					if cleaned_acronym not in acronyms_list or paper['findings'][i]['findingID'] not in findings_list:
						# appending a tuple of (acronym, finding number it was found in)
						if cleaned_acronym in filtered:
							full_acr_list.append((cleaned_acronym, paper['findings'][i]['findingID']))
		if full_acr_list != []:
			paper_body = clean_paper_body(paper['body'])
			doi = paper['DOI']
			sentences = [word_tokenize(s) for s in
			             sent_tokenize(paper_body)]  ##CW 20171009 Do Sent and word tokenization only once!
			for tuple in full_acr_list:
				findingID = tuple[1]
				acronym = tuple[0]
				acronym_definition = find_acronym_definitions(acronym, sentences)
				if acronym_definition != None:
					examplesa = examples.get(acronym, {})
					exlist = examplesa.get(acronym_definition, {})
					if len(
							exlist) < 5 and doi not in exlist:  # and newexample(paper['findings'][findingID]['captionBody'],exlist):
						print(acronym, '\t', acronym_definition, '\t', doi, '\t',
						      paper['findings'][findingID]['captionBody'])
						exlist[doi] = paper['findings'][findingID]['captionBody']
						examplesa[acronym_definition] = exlist
						examples[acronym] = examplesa
	return examples


# In[8]:

import json
import codecs

exdata = find_examples()
data_file = codecs.open('abbreviations_examples_v2.json', 'w', 'utf-8')
data_file.write(json.dumps(exdata, indent=2))
# json.dump(exdata,data_file)
data_file.close()

# In[ ]:
