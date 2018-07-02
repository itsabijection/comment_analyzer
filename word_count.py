#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 09:45:11 2018

@author: benjamin
"""
import dill as pickle
import re
from collections import defaultdict as dd
from nltk import word_tokenize, pos_tag
from nltk.probability import FreqDist as fd
import time
import sys
from os import getcwd
#from nltk.corpus import stopwords
site_list=["atlantic", "breitbart", "motherjones", "thehill"],
config_file=getcwd()+"/../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
direc_prefix=a[0]
result_storage_direc=a[1]
f.close()
serP=re.compile(r".*/(.*?)/comment")
day_finder=re.compile(r".*_(\d{1,3})\.txt")
year_finder=re.compile(r".*comments_(\d{4}).*")
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
def make_stats(low=None, hi=None,file_list=None, num_files=0, q=None):
    word_counts=dd(dd_of_dd_of_fd)
    word_POS_counts=dd(dd_of_dd_of_dd_of_fd)
    try:
        with open(result_storage_direc+"analysis_data"+str(low)+"-"+str(hi)+".pkl", "rb") as f:
            pass
    except:
        for i in range(low,hi):
            site=serP.search(file_list[i]).group(1)
            year=year_finder.search(file_list[i]).group(1)
            month=find_month(int(day_finder.search(file_list[i]).group(1)))
            q.put("{}. Started {} at {}".format(i,file_list[i], time.time()))
            print("{}. Started {} at {}".format(i,file_list[i], time.time()))
            try:
                with open(file_list[i], "rb") as comment_list_file:
                    comment_list=pickle.load(comment_list_file)
                    for comment in comment_list:
                        tagged_comment=pos_tag(word_tokenize(comment["raw_message"]))
                        for word_POS_pair in tagged_comment:
                                #well, the stemmer was working less well that i hoped
                                base_word=trim(word_POS_pair[0].lower())#stemmer.stem(word_POS_pair[0].lower())
                                word_counts[site][year][month][base_word]+=1
                                word_POS_counts[site][year][month][base_word][word_POS_pair[1]]+=1
            except:
                q.put("Problem with file"+file_list[i]+" "+sys.exc_info()[0])
            q.put("{}. Finished {} at {}".format(i,file_list[i], time.time()))
            print("{}. Finished {} at {}".format(i,file_list[i], time.time()))
        with open(result_storage_direc+"analysis_data"+str(low)+"-"+str(hi)+".pkl", "wb") as f:
            pickle.dump([word_counts, word_POS_counts], f)
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
