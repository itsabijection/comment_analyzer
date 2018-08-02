
from collections import defaultdict as dd
import dill as pickle
from nltk.stem import WordNetLemmatizer
lemmat=WordNetLemmatizer()

#merges two probability distributions of POS, and normalizes so add to 100%
#weighted by frequency of word usage
def merge(dist1, dist2, weight1, weight2):
    a=[0]*2
    a[0]=(dist1[0]*weight1+dist2[0]*weight2)/(weight1+weight2)
    a[1]=(dist1[1]*weight1+dist2[1]*weight2)/(weight1+weight2)
    c_s=a[0]+a[1]
    if c_s==0:
        return([0.5,0.5])
    m=1/c_s
    a=list(map(lambda x: x*m, a))
    return a

year="2016"
n=["NN","NNP","NNPS","NNS"]
adjs=["JJ","JJR","JJS"]
noun_p=dd(lambda: dd(lambda: [0]*12))
adj_p=dd(lambda: dd(lambda: [0]*12))
weights=dd(lambda: dd(lambda: [0]*12))
#other_p=dd(lambda: dd(lambda: [0]*12))
#direc="/home/banker/data/cleaner/"
direc="../data/2016/"
months=["Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
site_list=["atlantic","breitbart","thehill","motherjones"]
words=[]
        
num=0
ignore_list=[]
for i,month in enumerate(months):
    with open(direc+month+year+"stats.pkl","rb") as f:
        a=pickle.load(f)
        for word in a[1]["atlantic"][year][month].keys():
            num+=1
            for site in site_list:
                fr=a[0][site][year][month][word]
                if fr>10:
                    new_word=lemmat.lemmatize(word)
                    c=noun_p[site][new_word]
                    d=adj_p[site][new_word]
                    temp_n=sum([a[1][site][year][month][word].freq(p) for p in n])
                    temp_a=sum([a[1][site][year][month][word].freq(p) for p in adjs])
                    dist1=[noun_p[site][new_word][i], adj_p[site][new_word][i]]
                    dist2=[temp_n, temp_a]
                    weight1=weights[site][new_word][i]
                    weight2=fr
                    noun_p[site][new_word][i],adj_p[site][new_word][i]=merge(dist1,dist2,weight1,weight2)
                    weights[site][new_word][i]+=fr
                    #other_p[site][word][i]=sum([a[1][site][year][month][word].freq(p) for p in a[1][site][year][month][word].keys() if p not in n and p not in adjs])
                else:
                    ignore_list.append(word)
                    num-=1
                    break
            if num%1000==0:
                print(num)      
with open("../data/POSstats.pkl", "wb") as f:
    pickle.dump([noun_p, adj_p, ignore_list], f)