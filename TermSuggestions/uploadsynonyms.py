#import MySQLdb
#conn = MySQLdb.connect(host= "http://wp.hs-hannover.de",
#                  user="noa",
#                  passwd="456159729ed4",
#                  db="noa")
#cursor = conn.cursor()
##
#
#
#try:
#    with open("sim.txt") as fin:
#        for line in fin:
#            terms = line.split('\t')
#            for suggest in terms[1:]:
#                cursor.execute("""INSERT INTO synonyms VALUES (%s,%s)""",(terms[0],suggest))
#    conn.commit()
#except:
#    conn.rollback()
#
#conn.close()


fin = open("sim.txt","r")
fout = open("sim.csv","w")
for line in fin:
    terms = line.strip().split('\t')
    for suggest in terms[1:]:
        fout.write(terms[0]+'\t'+suggest+'\n')
fin.close()
fout.close()

            