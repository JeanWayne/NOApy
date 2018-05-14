import os

with open("C:\\NoaLines.txt", "w") as text_file:
	for root, dirs, files in os.walk('C:/NoaDocs_txt_v2/2004'):
		for file in files:
			with open(os.path.join(root, file), "r") as auto:
				a = auto.readlines()
				for line in a:
					l = line.replace('\n', '')

					# print(a)
					print(f"{l}\t{l}", file=text_file)
