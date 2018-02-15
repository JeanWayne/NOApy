#import math
import numpy as np
import requests
from nltk.stem import PorterStemmer

ps = PorterStemmer()

#def cosine(a,b):
#    return sum([a[k]*b[k] for k in range(len(a))]) / (math.sqrt(sum([a[k]**2 for k in range(len(a))])) * math.sqrt(sum([b[k]**2 for k in range(len(b))])))


def jaccard(A,B):
    schnitt = 0
    for a in A:
        if  a in B:
            schnitt += 1
    vereinigung = len(A) + len(B) - schnitt
    return float(schnitt)/float(vereinigung)
    
def ngram(string,n):
    liste = []
    if n < len(string):
        for p in range(len(string) - n + 1) :
            tg = string[p:p+n]
            liste.append(tg)
    return liste
    
def tgo(v,w):
    return jaccard(ngram('#'+v+'#',3),ngram('#'+w+'#',3))


words = []


response = requests.get(
        'http://VM1:8983/solr/NOA/terms',
        params={
            'terms.fl': 'spell-field',
            'terms.limit': '1000000',
            'terms.mincount':'12',
            'terms.maxcount':'50000'
        }
    )
   
   
indexterms = []

if(response.status_code == requests.codes.ok):
    rawindexterms = response.json()['terms']['spell-field']
    i = 0
    while i < len(rawindexterms):
        t  = rawindexterms[i]
        indexterms.append(t)
        i = i+2
 
print(len(indexterms), "terms retrieved from SOLR index") 

#with open("w2v_noa.txt") as fin:
with open("/root/jupyter/Gensim/w2v_noa.txt") as fin:
    for line in fin:
        w,v = line.split('\t')
        if w in indexterms:
            v = np.array(list(map(float,v.split())))
            v = v / np.linalg.norm(v)
            words.append((w,v))
        
print(len(words), "kept for comparison")
    
##local sensitive hashing
##put similar words into a bin. Compare only to words in the bin, if similarity to the first word is high enough
##start with one wor per bin. Reduce number of bins in the course of the computation

bins = [[i] for i in range(len(words))]
word2bin = {i:bins[i] for i in range(len(words)) }

fout = open("sim.txt","w")  
for i in range(len(words)):
    w,vec_w = words[i]
    if i % 1000 == 0:
        print(i, "words processed.")
        fout.flush()
        
    best = []
    for bin in bins:
        if bin == None:
            continue
        proto,vec_p = words[bin[0]]
        if proto == w:
            bsim  = 1
        else:
            bsim = np.dot(vec_w,vec_p.T)
        if bsim > 0.5:
            for i_x in bin[1:]:
                x,vec_x = words[i_x]
                sim = np.dot(vec_w,vec_x.T)                
                if (sim > 0.68 or (sim > 0.4 and tgo(w,x) > 0.4) ) and (len(best) < 5 or sim > best[4][1]) and ps.stem(w) != ps.stem(x):
                    best.append((x,sim))
                    best = sorted(best, key=lambda x: x[1], reverse=True)[:5]
            if (bsim > 0.68 or (bsim > 0.4 and tgo(w,proto) > 0.4)) and proto != w:
                if (len(best) < 5 or bsim > best[4][1]) and ps.stem(w) != ps.stem(proto):
                    best.append((proto,bsim))
                    best = sorted(best, key=lambda x: x[1], reverse=True)[:5]
                if bsim > 0.7 and len(bin) == 1 and bins[i] != None:
                    x = bin[0]
                    #print(x,i)
                    bins[i].append(x)
                    bins[x] = None
                    word2bin[x] = bins[i]
                    

            
    if len(best) > 0:
        fout.write(w+'\t')
        fout.write('\t'.join([b for b,v in best]))    
        fout.write('\n')
fout.close()