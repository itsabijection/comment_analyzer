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
import time
#from nltk.corpus import stopwords

site_list=["atlantic", "breitbart", "motherjones", "thehill"]
#site_list=["test1", "test2"]
direc_prefix="/home/benjamin/sfi/project_stuff/SFI_Comments_REU/sample/"
result_storage_direc="/home/benjamin/sfi/project_stuff/data/"

def trim(word):
    return(re.sub(r'[^A-Za-z \']', '', word))
    
#this is a hack to get around the fact that multiprocessing uses pickle 
#(instead of dill) and pickle can't handle lambdas
def dd_of_fd():
    return dd(fd)
def dd_of_dd_of_fd():
    return dd(dd_of_fd)
def dd_of_dd_of_dd_of_fd():
    return dd(dd_of_dd_of_fd)
#the lowth through the hith files. eg 210, 365 would be the last four months of the year.
#pipe is where to send the output instead of returning (if desired) and pattern
# is a regex of what file start to match. defaults to matching all comment files
def make_stats(low=None, hi=None, pipe=None, pattern=r'^comment.*', id_num=None):
    start=time.time()
    word_counts=dd(dd_of_dd_of_fd)
    word_POS_counts=dd(dd_of_dd_of_dd_of_fd)
    pattern=re.compile(pattern)
    try:
        f=open(result_storage_direc+"analysis_data"+str(id_num)+".pkl", "wb")
        d=pickle.load(f)
        word_counts=d[0]
        word_POS_counts=d[1]
        f.close()
    except:
        for site in site_list:
            direc=direc_prefix+site+"/"
            #slightly hacky. please fix
            i=0
            for filename in os.listdir(direc):
                if pattern.match(filename):
                    year=0
                    month=0
                    has_1000=re.compile(r".*?1000.*?")
                    if has_1000.match(filename):
                        year=filename[14:18]
                        month=find_month(int(filename[19:22]))
                    else:
                        year=filename[9:13]
                        month=find_month(int(filename[14:17]))
                    if hi is None or i in range(low, hi):
                        print("{} {}".format(direc_prefix+site+"/"+filename, id_num))
                        with open(direc+filename, "rb") as comment_list_file:
                            comment_list=pickle.load(comment_list_file)
                            for comment in comment_list:
                                tagged_comment=pos_tag(word_tokenize(comment["raw_message"]))
                                for word_POS_pair in tagged_comment:
                                        #was trimming, but i think that will just mess up
                                        #the tagging
                                        #well, the stemmer was working less well that i hoped
                                        base_word=trim(word_POS_pair[0].lower())#stemmer.stem(word_POS_pair[0].lower())
                                        word_counts[site][year][month][base_word]+=1
                                        word_POS_counts[site][year][month][base_word][word_POS_pair[1]]+=1
                    i+=1
    f=open(result_storage_direc+"analysis_data"+str(id_num)+".pkl", "wb")
    pickle.dump([word_counts, word_POS_counts], f)
    f.close()
    #if we called this as part of a multiprocess
    if pipe is not None:
        print("piping "+str(low)+" after time:")
        begin_piping=time.time()
        print(begin_piping-start)
        pipe.send([word_counts, word_POS_counts])
        #one gig test. under 2 seconds
        #pipe.send("0"*1000000000)
        pipe.close()
        print("time to pipe "+str(low)+":")
        print(time.time()-begin_piping)
    else:
        return [word_counts, word_POS_counts]

def find_month(day):
    days_per_month=[("Jan", 31),("Feb", 28), ("Mar", 31),("Apr", 30),("May", 31),("Jun",30),("Jul",31),("Aug", 31),("Sep", 30),("Oct", 31),("Nov",30),("Dec",31)]
    for month, i in days_per_month:
        day-=i
        if day<=0:
            return month

def proportional_diffs(word_counts, word_POS_counts):                                      
    word_diffs=dd(lambda : dd(int))
    #since i'm discarding words that don't get used at least a couple of time
    #across corpora "atlantic" could be any site (in fact, it should be the corpus with the least variety)
    for w in word_counts["atlantic"]:
        mi=min([word_counts[c].freq(w) for c in site_list])
        ma=max([word_counts[c].freq(w) for c in site_list])
        if abs(mi-ma)>0.005 and min([word_counts[c][w] for c in site_list])>3:
            word_diffs[w]=[{c: word_counts[c].freq(w)} for c in site_list]
