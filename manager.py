#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 15:33:43 2018

@author: benjamin
"""
import multiprocessing
from multiprocessing import Process, Queue
from word_count import make_stats
from logger import logger
import time
import os
import re
import random
import pickle
#import sys
start=time.time()
if __name__=="__main__":
    config_file=os.getcwd()+"/../locations.conf"
    f=open(config_file, "r")
    a=f.read().split("\n")
    direc_prefix=a[0]
    site_list=["atlantic", "breitbart", "motherjones", "thehill"]
    q=Queue()
    max_processes=multiprocessing.cpu_count()-1
    pattern=re.compile("^comment.*")
    file_list=[]
    for d in site_list:
        for i in os.listdir(direc_prefix+d+"/"):
            if pattern.match(i):
                file_list.append(direc_prefix+d+"/"+i)
    num_files=len(file_list)
    to_each=int(num_files/max_processes)
    remainder=num_files-to_each*max_processes
    processes=[]
    hi=0
    #shuffle so the large files aren't next to each other
    random.shuffle(file_list)
    result_storage_direc=a[1]
    with open(result_storage_direc+"file_order.pkl", "wb") as f:
            pickle.dump(file_list, f)
    log_process=Process(target=logger, args=(q,))
    log_process.start()
    for i in range(max_processes):
        low=hi
        hi=low+to_each
        if remainder>0:
            hi+=1
            remainder-=1
        if hi>num_files:
            break
        processes.append(Process(target=make_stats, args=(low, hi, file_list, num_files, q), daemon=True))
        processes[i].start()
    for i in processes:
        i.join()
    q.put("kill")
end=time.time()
print("total time:")
print(end-start)


