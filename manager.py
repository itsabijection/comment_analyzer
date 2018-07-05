#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 15:33:43 2018

@author: benjamin
"""
from multiprocessing import Process, Queue, cpu_count
from word_count import make_stats
from nltk.probability import FreqDist as fd
from collections import defaultdict as dd
from logger import logger
import dill as pickle
import time
import os
import re

config_file=os.getcwd()+"/../locations.conf"
f=open(config_file, "r")
a=f.read().split("\n")
direc_prefix=a[0]
site_list=["atlantic", "breitbart", "motherjones", "thehill"]
result_storage_direc=a[1]

max_processes=cpu_count()-1

pattern=re.compile("^comment.*")
files=[]
for d in site_list:
    for i in os.listdir(direc_prefix+d+"/"):
        if pattern.match(i):
            files.append(direc_prefix+d+"/"+i)
            
#site, year, month, word
word_counts=dd(lambda: dd(lambda: dd(fd)))
#site, year, month, word, POS
word_POS_counts=dd(lambda: dd(lambda: dd(lambda: dd(fd))))

start=time.time()
if __name__=="__main__":
    file_q  = Queue()
    log_q   = Queue()
    stats_q = Queue()
    processed=[]
    for i in files:
        file_q.put(i)
    log_process=Process(target=logger, args=(log_q,))
    log_process.start()
    processes=[]
    for i in range(max_processes):
        processes.append(Process(target=make_stats, args=(log_q, file_q, stats_q, i), daemon=True))
        processes[i].start()
    for i in range(len(files)):
        if i>0 and i%10==0:
            with open(result_storage_direc+"intermediate.pkl", "wb") as f:
                pickle.dump([word_counts, word_POS_counts, processed], f)
        [partial_word_counts, partial_word_POS_counts, site, year, month, done_file]=stats_q.get()
        processed.append(done_file)
        for w in partial_word_counts.keys():
            word_counts[site][year][month][w]+=partial_word_counts[w]
        for w in partial_word_POS_counts.keys():
            for p in partial_word_POS_counts[w].keys():
                word_POS_counts[site][year][month][w][p]+=partial_word_POS_counts[w][p]
    with open(result_storage_direc+"stats.pkl", "wb") as f:
            pickle.dump([word_counts, word_POS_counts], f)
    for i in processes:
        i.join()
    log_q.put("kill")
end=time.time()
print("total time:")
print(end-start)


