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
    max_processes=2
    num_files=2
    pipes=[]
    processes=[]
    for i in range(max_processes):
        pipes.append(Pipe(duplex="False"))
        processes.append(Process(target=make_stats, args=(int(num_files/max_processes)*i,int(num_files/max_processes)*(i+1), pipes[i][1])))
        processes[i].start()
    for i in pipes:
        print(i[0].recv()[0:2])
end=time.time()
print("total time:")
print(end-start)