#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 14:01:03 2018

@author: benjamin
"""

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
import gc
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

def make_stats(log_q, file_q, stats_q, i, kill_q):
        while not file_q.empty() and kill_q.empty():
            c_file=file_q.get()
            word_counts=fd()
            word_POS_counts=dd(fd)
            site=serP.search(c_file).group(1)
            year=year_finder.search(c_file).group(1)
            month=find_month(int(day_finder.search(c_file).group(1)))
            log_q.put("Started {} at {}".format(c_file, time.time()))
#            print("Started {} at {}".format(c_file, time.time()))
            try:
                with open(c_file, "rb") as comment_list_file:
                    comment_list=pickle.load(comment_list_file)
                    for comment in comment_list:
                        tagged_comment=pos_tag(word_tokenize(comment["raw_message"]))
                        for word_POS_pair in tagged_comment:
                                base_word=trim(word_POS_pair[0].lower())#stemmer.stem(word_POS_pair[0].lower())
                                word_counts[base_word]+=1
                                word_POS_counts[base_word][word_POS_pair[1]]+=1
            except:
                log_q.put("Problem with file "+c_file+" "+str(sys.exc_info()[0]))
            log_q.put("Finished {} at {}".format(c_file, time.time()))
#            print("Finished {} at {}".format(c_file, time.time()))
            stats_q.put([word_counts, word_POS_counts, site, year, month, c_file])
            gc.collect()

def find_month(day):
    days_per_month=[("Jan", 31),("Feb", 28), ("Mar", 31),("Apr", 30),("May", 31),("Jun",30),("Jul",31),("Aug", 31),("Sep", 30),("Oct", 31),("Nov",30),("Dec",31)]
    for month, i in days_per_month:
        day-=i
        if day<=0:
            return month
