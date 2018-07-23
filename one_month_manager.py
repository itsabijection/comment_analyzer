#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 15:33:43 2018

@author: benjamin
"""
from multiprocessing import Process, Queue
from word_count import make_stats, find_month
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
max_processes=18
months=["Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][::-1]
day_finder=re.compile(r".*_(\d{1,3})\.txt")
year_finder=re.compile(r".*comments_.*?(\d{4})_\d{1,3}.*")
pattern=re.compile(r"comments(_1000)?_2015.*?")
files=dd(list)
for d in site_list:
    for i in os.listdir(direc_prefix+d+"/"):
        if pattern.match(i):
            files[find_month(int(day_finder.search(i).group(1)))].append(direc_prefix+d+"/"+i)
#print(files)
processed=[]
start=time.time()
if __name__=="__main__":
    for r in months:
        #site, year, month, word
        word_counts=dd(lambda: dd(lambda: dd(fd)))
        #site, year, month, word, POS
        word_POS_counts=dd(lambda: dd(lambda: dd(lambda: dd(fd))))
        file_q  = Queue()
        log_q   = Queue()
        stats_q = Queue()
        kill_q  = Queue()
        for i in files[r]:
            file_q.put(i)
        #print(file_q)
        log_process=Process(target=logger, args=(log_q,))
        log_process.start()
        processes=[]
        for i in range(max_processes):
            processes.append(Process(target=make_stats, args=(log_q, file_q, stats_q, i), daemon=True))
            processes[i].start()
        for i in range(len(files[r])):
            [partial_word_counts, partial_word_POS_counts, site, year, month, done_file, p]=stats_q.get()
            for w in partial_word_counts.keys():
                word_counts[site][year][month][w]+=partial_word_counts[w]
            for w in partial_word_POS_counts.keys():
                for p in partial_word_POS_counts[w].keys():
                    word_POS_counts[site][year][month][w][p]+=partial_word_POS_counts[w][p]
            if i>0 and i%10==0:
                with open(result_storage_direc+r+"intermediate"+str(i)+".pkl", "wb") as f:
                    pickle.dump([word_counts, word_POS_counts, processed], f)
                if i>20:
                    os.remove(result_storage_direc+r+"intermediate"+str(i-20)+".pkl")
            kill_q.put("Done")
        with open(result_storage_direc+r+"2015stats.pkl", "wb") as f:
                pickle.dump([word_counts, word_POS_counts], f)
        log_q.put("kill")
        for i in processes:
            i.join()
end=time.time()
print("total time:")
print(end-start)


