

fin = open("sim.txt","r")
fout = open("sim.sql","w")

fout.write("DELETE FROM synonyms;\n\n")

fout.write("INSERT INTO synonyms (term, suggestion)\nVALUES\n")

terms = fin.readline().strip().split('\t')
fout.write("('"+terms[0]+"','"+terms[1]+"')")
for suggest in terms[2:]:
        fout.write(",\n('"+terms[0]+"','"+suggest+"')")

for line in fin:
    terms = line.strip().split('\t')
    for suggest in terms[1:]:
        fout.write(",\n('"+terms[0]+"','"+suggest+"')")
fout.write(";")   
  
        
fin.close()
fout.close()

            