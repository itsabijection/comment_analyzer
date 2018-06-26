#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 15:33:43 2018

@author: benjamin
"""

from multiprocessing import Process, Pipe
from word_count import make_stats
import time

start=time.time()
if __name__=="__main__":
    max_processes=3
    num_files=3
    #num_files differs across corpora unfortunately, but 2415 is the max. 
    #with 24 cores this means chunks of 400 files, and at 30seconds/file that's
    #approximately 3.3 hours. doubling that for safety means ~7
    pipes=[]
    processes=[]
    res=[]
    for i in range(max_processes):
        pipes.append(Pipe(duplex="False"))
        processes.append(Process(target=make_stats, args=(int(num_files/max_processes)*i,int(num_files/max_processes)*(i+1), pipes[i][1], r'^comments_2017.*', i)))
        processes[i].start()
    for i in pipes:
        res.append(i[0].recv()[:])
end=time.time()
print("total time:")
print(end-start)


