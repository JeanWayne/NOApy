import codecs
import json

import nltk

loc_for_abb = 'abbreviations_examples_v2.json'

with codecs.open(loc_for_abb, 'r', 'utf-8') as data_file:
	# for l in data_file:
	abbreviations = json.loads(data_file.read())

# with codecs.open('abb_'+ str(int(datetime.now(tz=timezone.utc).timestamp() * 1000))+'.txt', 'w', 'utf-8') as the_file:
# 	the_file.write('Abr\tDef\tDoi\tExample\n')
# 	# Abr	Def	Doi	Example
# 	j=0
# 	k=0
# 	l=0
# 	for ab in abbreviations:
# 		# print(ab)
# 		# the_file.write(ab+"\t")
# 		j+=1
# 		for sol in abbreviations[ab]:
# 			# print(sol)
# 			# the_file.write(sol + "\t")
# 			k+=1
# 			for doi in abbreviations[ab][sol]:
# 				# print(doi)
# 				# print(abbreviations[ab][sol][doi])
# 				# the_file.write(doi + "\t")
# 				the_file.write(ab + "\t" + sol + "\t" + doi + "\t" + abbreviations[ab][sol][doi] + "\n")
# 				l+=1
# 				# print(len(abbreviations['EECP']))
# print(j,k,l)

with codecs.open('abb_1521047089902.txt', 'r', 'utf-8') as the_file:
	st = the_file.readlines()
	abku = []
	auf = []
	tok = []
	for l in st:
		d = l.split('\t')
		if len(d) < 3:
			continue
		abku.append(d[0])
		auf.append(d[1])
		for s in nltk.word_tokenize(d[3]):
			tok.append(s)

	print(len(set(abku)))
	print(len(set(auf)))
	print(len(set(tok)))
