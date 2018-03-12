import codecs
import json

loc_for_abb = 'abbreviations_examples_07_03_2018.json'

with codecs.open(loc_for_abb, 'r', 'utf-8') as data_file:
	for l in data_file:
		abbreviations = json.loads(l)

with codecs.open('3er_abb.txt', 'a', 'utf-8') as the_file:
	the_file.write('Abr\tDef\tDoi\tExample\n')
	# Abr	Def	Doi	Example
	for ab in abbreviations:
		# print(ab)
		# the_file.write(ab+"\t")
		for sol in abbreviations[ab]:
			# print(sol)
			# the_file.write(sol + "\t")
			for doi in abbreviations[ab][sol]:
				# print(doi)
				# print(abbreviations[ab][sol][doi])
				# the_file.write(doi + "\t")
				the_file.write(ab + "\t" + sol + "\t" + doi + "\t" + abbreviations[ab][sol][doi] + "\n")

				# print(len(abbreviations['EECP']))
