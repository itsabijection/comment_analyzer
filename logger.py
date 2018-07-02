#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:50:11 2018

@author: benjamin
"""
import os
logfile="/home/benjamin/sfi/project_stuff/data/word_count.log"
def logger(q):
    f=open(logfile, "w")
    while True:
        m=q.get()
        #if the parent tell logger to kill itself or the parent
        #has been killed/has died
        if m=="kill" or os.getppid()==1:
            break
        f.write(str(m) + "\n")
        f.flush()
    f.close()