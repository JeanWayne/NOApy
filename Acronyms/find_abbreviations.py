import time

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, WhitespaceTokenizer

wnl = WordNetLemmatizer()
from nltk import word_tokenize
from pymongo import MongoClient

tokenizer = WhitespaceTokenizer()
import re

## John's local host section
# client = MongoClient()
# db = client.NLP
# collection = db.wiki

# Christian's server section
client = MongoClient('mongodb://141.71.5.19:27017/')
db = client.beta
collection = db.hindawi_1505118371032
collection = db.Corpus_Playground

has_finding = collection.find({'numOfFindings': {'$gt': 0}})

# dictionary of dictionary
journal_abr_dict = {}

total_time = time.time()
start = time.time()
# this section tries to find the definition of a given abbrev.
# input is a list of sentences, andhanumeric letters, periods and dashes
abr_in_abr_counter = 0


def find_abbrev_definitions(abbreviation, sent_list):
	global abr_in_abr_counter
	for words_list in sent_list:  # CW 20171009
		if (abbreviation in words_list):
			# iterate over a collection of words to see if they contain the abbreviation
			for idx_word_list in range(len(words_list)):
				# if abbreviation exists and is surrounded by parenthesis
				if abbreviation == words_list[idx_word_list] and '(' in words_list[(idx_word_list - 1)] and ')' in \
						words_list[idx_word_list + 1]:
					boo = True
					abr_len = len(abbreviation)
					for idx_abrev in range(abr_len):

						# minus one to get over the parenthesis
						if abbreviation[idx_abrev] != words_list[idx_word_list + idx_abrev - abr_len - 1][0].upper():

							# here we will check to see if there are abbreviations in the abbreviation definition
							# if the word is all upper case

							# if the first check is a negative, it is possible there is an abbreviation somwhere
							# in the definition of the abbreviation, so we will check for that.  No need to
							start = idx_word_list + idx_abrev - abr_len
							end = idx_word_list - 1  # minus 1 to get over parentheses
							for a in range(start, end):
								if len(words_list[a]) > 1 and words_list[a] in abbreviation and words_list[
									a] != abbreviation:
									tmp_abr = re.sub(words_list[a], '', abbreviation)  # remove inner abrev from abbrev
									tmp_wrd_list = words_list[:a] + words_list[a + 1:]  # remove inner abbrev from list
									tmp_abr_len = len(tmp_abr)

									for tmp_idx_abrev in range(tmp_abr_len):
										# have to subtract an extra 1 because we decreased word list size by 1
										if tmp_abr[tmp_idx_abrev] != \
												tmp_wrd_list[idx_word_list + tmp_idx_abrev - tmp_abr_len - 2][
													0].upper():
											boo = False
											break
									if boo:
										abr_in_abr_counter += 1

										out = ' '.join(str(x) for x in
										               (words_list[idx_word_list - tmp_abr_len - 2:idx_word_list - 1]))
										return (out)

									else:
										return (None)
							# RNA polymerase (RNAP)
							# print('abbreviation in the abbreviation')
							# print(' '.join(words_list[idx_word_list - 6:idx_word_list + 3]))
							# print(words_list[idx_word_list + idx_abrev - abr_len - 1])
							boo = False
							break

					if boo:
						out = ' '.join(str(x) for x in (words_list[idx_word_list - idx_abrev - 2:idx_word_list - 1]))
						return (out)
	return (None)


# used to clean up the body text
def clean_paper_body(body1):
	# change a hypenated word into two words
	body2 = re.sub('-|\n|\t', ' ', body1)
	# remove all periods.  Current coding scheme wouldn't catch arconyms such as "G.R.B", so if we remove periods
	# we can catch it as "GRB"
	cleaned = re.sub('\.', '', body2)
	return cleaned


# used for statistics
counter = 0
total_papers = 0
paper_counter = 0
positive_total_found = 0
total_abbreviations = 0

# journal name is used as the key
dict_of_journals = {}

######################################################
# find all abbreviations and definitions
######################################################
# print("Stage 1")


# dictionary of dictionaries, with the journal name as the first key
# and the abbrev as the second key.
# The value is then a list of definitions.
for paper in has_finding:
	total_papers += 1
	if 'body' not in paper or not isinstance(paper['body'], str):
		continue
	full_abr_list = []
	# list of finding indexes
	findings_list = []

	# goes through each image caption
	for i in range(len(paper['findings'])):
		cleaned_body = ""
		if (paper['findings'][i]['captionBody'] != None):
			# clean all but alphanumeric letters, periods and dashes
			cleaned_body = re.sub('[^A-Za-z.-]', ' ', paper['findings'][i]['captionBody'])
		tok_body = tokenizer.tokenize(cleaned_body)
		for abr in tok_body:
			# remove periods, and leading/tailing dashes
			cleaned_abbreviation = re.sub('\-|\.|-$', '', abr)
			if cleaned_abbreviation.isupper() and len(cleaned_abbreviation) > 2:
				abr_list = [item[0] for item in full_abr_list]
				findings_list = [item[1] for item in full_abr_list]
				if cleaned_abbreviation not in abr_list or paper['findings'][i]['findingID'] not in findings_list:
					# appending a tuple of (abbrev, finding number it was found in)
					full_abr_list.append((cleaned_abbreviation, paper['findings'][i]['findingID']))
	if full_abr_list != []:
		# used for statistics
		paper_counter += 1
		paper_body = clean_paper_body(paper['body'])
		sentences = [word_tokenize(s) for s in
		             sent_tokenize(paper_body)]  ##CW 20171009 Do Sent and word tokenization only once!
		for tuple in full_abr_list:
			findingID = tuple[1]
			abbrev = tuple[0]
			abbrev_def = find_abbrev_definitions(abbrev, sentences)

			if abbrev_def != None:
				positive_total_found += 1
			total_abbreviations += 1

			if paper['journalName'] not in dict_of_journals:
				dict_of_journals[paper['journalName']] = {abbrev: [[abbrev_def, findingID, paper['_id']]]}
			else:
				try:
					dict_of_journals[paper['journalName']][abbrev].append([abbrev_def, findingID, paper['_id']])
				except KeyError:
					dict_of_journals[paper['journalName']].update({abbrev: [[abbrev_def, findingID, paper['_id']]]})

print('total papers searched: ', total_papers)
print('total abbreviations added: ', total_abbreviations)
print('total positive abbreviations found: ', positive_total_found)
print("time:", time.time() - start)
print('new abbreviation found where an \n'
      'abbreviation was in the definition: ', abr_in_abr_counter)
######################################################
# updating mongodb with all results
######################################################
print('Stage 3')

for journal_key, abr_dictionary in dict_of_journals.items():
	# abr is the abbrev
	# def_findID_paperID is a list of lists containing [abr definition, findingID, paperID]
	for abr_key, def_findID_paperID in abr_dictionary.items():
		for row in def_findID_paperID:
			abr_def = row[0]
			findingID = row[1]
			paperID = row[2]
			if abr_def != None:
				collection.update({'_id': paperID},
				                  {'$addToSet': {'findings.' + str(findingID) + '.acronym': (abr_key, abr_def)}},
				                  upsert=False, multi=True)
			# no definition found so add None as the definition
			else:
				collection.update({'_id': paperID},
				                  {'$addToSet': {'findings.' + str(findingID) + '.acronym': (abr_key, None)}},
				                  upsert=False, multi=True)
print("total time (with mongodb update):", time.time() - total_time)
