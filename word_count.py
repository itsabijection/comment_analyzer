#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 09:45:11 2018

@author: benjamin
"""
import dill as pickle
import os
import re
from collections import defaultdict as dd
from nltk import word_tokenize, pos_tag
from nltk.probability import FreqDist as fd
from nltk.stem.snowball import SnowballStemmer
import time
#from nltk.corpus import stopwords

def trim(word):
    return(re.sub(r'[^A-Za-z \']', '', word))

start=time.time()
a=0
stemmer=SnowballStemmer("english")
site_list=["atlantic", "breitbart", "motherjones", "thehill"]
direc_prefix="/home/benjamin/sfi/project_stuff/SFI_Comments_REU/sample/"
word_counts=dd(fd)
word_POS_counts=dd(lambda: dd(fd))
for site in site_list:
    direc=direc_prefix+site+"/"
    for filename in os.listdir(direc):
        if filename.startswith("comment"):
            with open(direc+filename, "rb") as comment_list_file:
                comment_list=pickle.load(comment_list_file)
                for comment in comment_list:
                    tagged_comment=pos_tag(word_tokenize(comment["raw_message"]))
                    for word_POS_pair in tagged_comment:
                            #was trimming, but i think that will just mess up
                            #the tagging
                            base_word=trim(word_POS_pair[0].lower())#stemmer.stem(word_POS_pair[0].lower())
                            word_counts[site][base_word]+=1
                            word_POS_counts[site][base_word][word_POS_pair[1]]+=1
                            a+=1
                            if a==100000:
                                end=time.time()
                                print(end-start)
                            
#%%                          
word_diffs=dd(lambda : dd(int))
#since i'm discarding words that don't get used at least a couple of time
#across corpora "atlantic" could be any site (in fact, it should be the corpus with the least variety)
for w in word_counts["atlantic"]:
    mi=min([word_counts[c].freq(w) for c in site_list])
    ma=max([word_counts[c].freq(w) for c in site_list])
    if abs(mi-ma)>0.005 and min([word_counts[c][w] for c in site_list])>3:
        word_diffs[w]=[{c: word_counts[c].freq(w)} for c in site_list]
#%%    
pickle.dump([word_counts, word_POS_counts], open("/home/benjamin/sfi/project_stuff/data/word_diffs.pkl", "wb"))