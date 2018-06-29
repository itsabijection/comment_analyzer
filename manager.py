#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 15:33:43 2018

@author: benjamin
"""
import multiprocessing
from multiprocessing import Process
from word_count import make_stats
import time
import os
import re
import random
#import sys
start=time.time()
if __name__=="__main__":
    direc_prefix="/home/benjamin/sfi/project_stuff/SFI_Comments_REU/sample/"
    site_list=["atlantic", "breitbart", "motherjones", "thehill"]
    max_processes=multiprocessing.cpu_count()
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
    for i in range(max_processes):
        low=hi
        hi=low+to_each
        if remainder>0:
            hi+=1
            remainder-=1
        if hi>num_files:
            break
        processes.append(Process(target=make_stats, args=(low, hi, file_list, num_files), daemon=True))
        processes[i].start()
    for i in processes:
        i.join()
end=time.time()
print("total time:")
print(end-start)


